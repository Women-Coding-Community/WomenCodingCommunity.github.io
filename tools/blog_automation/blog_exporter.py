import argparse
import json
import os
import re
import shutil
import datetime as dt
from pathlib import Path
import bleach
import markdown
import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# --- Configuration ---
SERVICE_ACCOUNT_FILE = 'service_account_key.json'
# Used when a submission's cover image can't be downloaded (missing/not shared).
DEFAULT_IMAGE_PATH = '/assets/images/blog/default.jpg'

# Allowlist for sanitizing HTML converted from submitted Google Docs. Covers the
# formatting blog posts need; everything else (scripts, iframes, event handlers,
# etc.) is stripped. See _markdown_to_html.
ALLOWED_TAGS = [
    'p', 'br', 'hr', 'span',
    'strong', 'b', 'em', 'i', 'u', 's', 'sub', 'sup', 'small', 'mark',
    'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'ul', 'ol', 'li', 'dl', 'dt', 'dd',
    'a', 'img',
    'code', 'pre', 'blockquote',
    'table', 'thead', 'tbody', 'tr', 'th', 'td', 'caption',
]
ALLOWED_ATTRIBUTES = {
    'a': ['href', 'title', 'rel'],
    'img': ['src', 'alt', 'title'],
}
ALLOWED_PROTOCOLS = ['http', 'https', 'mailto']
YAML_HEADER = '''---
layout: post
title: {title}
date: {date}
author_name: {author_name}
author_role: {author_role}
image: {image_path}
image_source: {image_source}
description: {description}
category: blog
---
'''

def _yaml_scalar(value):
    """Return a YAML-safe double-quoted scalar.

    Free-text fields (title, description, ...) can contain ``:``, ``&``, quotes
    etc. that break unquoted YAML front matter. A JSON-encoded string is always a
    valid YAML double-quoted scalar, so json.dumps gives us correct escaping.
    """
    return json.dumps('' if value is None else str(value), ensure_ascii=False)

def _current_directory():
    return os.path.dirname(os.path.abspath(__file__))

def drive_connection():
    service_account_path = os.path.join(_current_directory(), SERVICE_ACCOUNT_FILE)
    if not os.path.exists(service_account_path):
        print(f"ERROR: Service account key file '{service_account_path}' not found.\n"
              "Please obtain your own Google service account key and place it at this path.\n"
              "(Never commit this file to version control.)")
        exit(1)
    creds = service_account.Credentials.from_service_account_file(
        service_account_path, 
        scopes=['https://www.googleapis.com/auth/drive.readonly']
    )
    drive = build('drive', 'v3', credentials=creds)
    return drive

def _posts_directory():
    script_dir = Path(_current_directory())
    posts_dir = (script_dir / "../../_posts").resolve()
    return posts_dir

def _today_date_str():
    return dt.date.today().isoformat()

def _create_blog_filename_with_date(doc_name, date_str):
    # Slugify: lowercase, and collapse any run of non-alphanumeric characters
    # (spaces, ':', ',', etc.) into a single hyphen so the filename is valid.
    slug = re.sub(r'[^a-z0-9]+', '-', doc_name.lower()).strip('-')
    return f"{date_str}-{slug}"

def _get_doc_name_from_drive(doc_id, drive):
    """Fetch document name from Google Drive."""
    try:
        file = drive.files().get(fileId=doc_id, fields='name').execute()
        return file['name']
    except HttpError as error:
        print(f"ERROR: Could not fetch document from Drive (ID: {doc_id})\n{error}")
        return None

def _get_doc_content_as_markdown(doc_id, drive):
    """Export Google Doc as markdown."""
    try:
        request = drive.files().export_media(fileId=doc_id, mimeType='text/markdown')
        file_content = request.execute()
        return file_content.decode('utf-8')
    except HttpError as error:
        print(f"ERROR: Could not export document from Drive (ID: {doc_id})\n{error}")
        return None

def _markdown_to_html(markdown_text):
    """Convert Markdown to HTML with custom formatting.

    Blog content comes from community-submitted Google Docs, which can contain
    arbitrary raw HTML. We sanitize the converted HTML against an explicit
    allowlist so a submitted document cannot inject <script>, event handlers or
    javascript: URLs into the published (public) site.
    """
    html = markdown.markdown(markdown_text)

    # Remove <strong> tags from inside heading tags
    html = re.sub(r'<h(\d)><strong>(.+?)</strong></h\1>', r'<h\1>\2</h\1>', html)

    # Remove the first heading if present
    html = re.sub(r'^<h[1-6]>.*?</h[1-6]>\s*', '', html, flags=re.DOTALL)

    # Strip anything outside the allowlist (drops <script>, on* handlers, etc.)
    html = bleach.clean(
        html,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        protocols=ALLOWED_PROTOCOLS,
        strip=True,
    )

    # Wrap the body in <div class="text-justify"> (added after sanitizing, so the
    # wrapper we control is never stripped).
    html_body = f'<div class="text-justify">\n{html}\n</div>'

    return html_body

def _download_blog_image(blog_image_drive_link, drive):
    """Download image from Google Drive link."""

    pattern = re.compile(r"(?:id=|/d/)([^/&?]+)")

    try:
        file_id = re.search(
            pattern,
            blog_image_drive_link
        )
        if not file_id:
            raise Exception(f"WARNING: Could not extract file ID from image link: {blog_image_drive_link}")
        
        file_id = file_id.group(1)
        print(f'{file_id=}')
        file_metadata = drive.files().get(fileId=file_id, fields='name, mimeType').execute()
        file_name = file_metadata['name']

        mime_type = file_metadata.get('mimeType', '')
        if not mime_type.startswith('image/'):
            print(f"WARNING: cover file is '{mime_type}', not an image ({file_name}); skipping.")
            return None

        request = drive.files().get_media(fileId=file_id)
        file_content = request.execute()
        
        # Save temporarily
        temp_path = os.path.join(_current_directory(), file_name)
        with open(temp_path, 'wb') as f:
            f.write(file_content)
        
        return temp_path
    except HttpError as error:
        print(f"WARNING: Could not download image from Drive\n{error}")
        return None

def _copy_image_to_blog_assets(image_path, blog_filename):
    """Copy image to assets directory and return relative path."""
    if not image_path or not os.path.exists(image_path):
        return None
    
    assets_dir = Path(_current_directory()).resolve().parent.parent / 'assets' / 'images' / 'blog'
    assets_dir.mkdir(parents=True, exist_ok=True)

    new_image_filename = blog_filename.split('.')[0] + '.' +image_path.split('.')[-1]
    new_image_path = assets_dir / new_image_filename

    shutil.copy(image_path, new_image_path)
    
    return f"/assets/images/blog/{new_image_filename}"

# def _get_image_path_from_blog_filename_and_image_extension(blog_filename, image_extension):
#     assets_dir = Path(_current_directory()).resolve().parent.parent / 'assets' / 'images' / 'blog'
#     image_filename = assets_dir / (blog_filename.split('.')[0] + image_extension)
#     return image_filename

def download_image_and_copy_to_repo(image_link, blog_filename, drive):
    downloaded_image_path = _download_blog_image(image_link, drive)
    if downloaded_image_path is None:
        # Image missing or not shared with the service account; caller falls back
        # to the default cover image.
        return None

    image_path_relative = _copy_image_to_blog_assets(
        downloaded_image_path,
        blog_filename
    )

    os.remove(downloaded_image_path)  # Clean up temp file

    return image_path_relative


def export_blog(blog_info, date=None, doc_id_override=None):
    """
    Export a single blog into a Jekyll post (HTML) plus its cover image.

    Args:
        blog_info: Mapping (dict / pandas Series) with the keys produced by
            blog_info_from_spreadsheet._extract_and_rename_relevant_fields:
            doc_id, author_name, author_role, description, source, image_link.
        date: Blog post date (defaults to today).
        doc_id_override: Optional Google Doc ID to use instead of blog_info['doc_id'].

    Returns:
        blog_filename if successful, None otherwise.
    """
    if date is None:
        date = _today_date_str()

    blog_info_ser = blog_info

    # Determine doc_id
    doc_id = doc_id_override or blog_info_ser.get('doc_id')

    if pd.isna(doc_id) or not doc_id:
        print("SKIP: row has no doc_id (external blog link)")
        raise ValueError("No doc_id found in spreadsheet row. Please specify a doc_id_override.")

    # Connect to Google Drive
    drive = drive_connection()
    
    # 1. Get document name and content
    doc_name = _get_doc_name_from_drive(doc_id, drive)
    doc_content = _get_doc_content_as_markdown(doc_id, drive)
    if doc_name is None or doc_content is None:
        raise ValueError(
            f"Could not fetch Google Doc {doc_id} - it may not exist, not be a "
            f"native Google Doc, or not be shared with the service account."
        )
    blog_filename = _create_blog_filename_with_date(doc_name, date)
    
    # 2. Convert to HTML
    html_body = _markdown_to_html(doc_content)
    
    # 3. Build YAML header
    author_name = blog_info_ser.get('author_name', 'Unknown')
    author_role = blog_info_ser.get('author_role', '')
    description = blog_info_ser.get('description', '')
    source = blog_info_ser.get('source', '')

    
    yaml_header = YAML_HEADER.format(
        title=_yaml_scalar(doc_name),
        date=date,
        author_name=_yaml_scalar(author_name),
        author_role=_yaml_scalar(author_role),
        image_path='[IMAGE_PATH]',  # Placeholder, will update after image download
        image_source=_yaml_scalar(source),
        description=_yaml_scalar(description)
    )
    
    # 4. Download cover image; fall back to the default if it's missing or not
    #    shared with the service account, so a bad image never blocks the post.
    image_path_relative = None
    image_link = blog_info_ser.get('image_link')
    if image_link:
        image_path_relative = download_image_and_copy_to_repo(
            image_link, blog_filename=blog_filename, drive=drive
        )
    if not image_path_relative:
        print(f"WARNING: no usable cover image for '{doc_name}'; using default cover.")
        image_path_relative = DEFAULT_IMAGE_PATH
    yaml_header = yaml_header.replace('[IMAGE_PATH]', image_path_relative)

    # 5. Combine and save
    final_html = yaml_header + '\n' + html_body
    
    posts_dir = _posts_directory()
    posts_dir.mkdir(parents=True, exist_ok=True)
    
    filename = posts_dir / f"{blog_filename}.html"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(final_html)
    
    print(f"✓ Exported blog to: {filename}")
    return blog_filename


if __name__ == "__main__":
    # Ad-hoc single-blog export, handy for testing a Google Doc renders correctly:
    #   python blog_exporter.py --doc_id <DOC_ID> --author_name "Jane Doe"
    parser = argparse.ArgumentParser(description="Export a single blog Doc into an HTML post.")
    parser.add_argument("--doc_id", required=True, help="Google Doc ID to export.")
    parser.add_argument("--author_name", default="")
    parser.add_argument("--author_role", default="")
    parser.add_argument("--description", default="")
    parser.add_argument("--source", default="")
    parser.add_argument("--image_link", default="", help="Google Drive link to the cover image.")
    parser.add_argument("--date", help="Date for blog post (YYYY-MM-DD). Defaults to today.")

    args = parser.parse_args()
    export_blog(
        {
            "doc_id": args.doc_id,
            "author_name": args.author_name,
            "author_role": args.author_role,
            "description": args.description,
            "source": args.source,
            "image_link": args.image_link,
        },
        date=args.date,
    )
