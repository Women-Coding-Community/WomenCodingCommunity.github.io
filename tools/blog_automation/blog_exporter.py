import argparse
import os
import re
import shutil
import datetime as dt
from pathlib import Path
import markdown
import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# --- Configuration ---
SERVICE_ACCOUNT_FILE = 'service_account_key.json'
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
    formatted_blog_title = doc_name.lower().replace(' ', '-').strip()
    filename = f"{date_str}-{formatted_blog_title}"
    return filename

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
    """Convert Markdown to HTML with custom formatting."""
    html = markdown.markdown(markdown_text)
    
    # Remove <strong> tags from inside heading tags
    html = re.sub(r'<h(\d)><strong>(.+?)</strong></h\1>', r'<h\1>\2</h\1>', html)
    
    # Remove the first heading if present
    html = re.sub(r'^<h[1-6]>.*?</h[1-6]>\s*', '', html, flags=re.DOTALL)
    
    # Wrap the body in <div class="text-justify">
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
    # if downloaded_image_path is not None:
    #     image_path_relative = _get_image_path_from_blog_filename_and_image_extension(
    #         blog_filename, image_extension=downloaded_image_path.split('.')[-1]
    #     )

    image_path_relative = _copy_image_to_blog_assets(
        downloaded_image_path, 
        blog_filename
    )

    os.remove(downloaded_image_path)  # Clean up temp file
    
    return image_path_relative


def export_blog_from_csv_row(row_index, csv_path=None, doc_id_override=None, date=None):
    """
    Export a blog from a CSV row.
    
    Args:
        row_index: Index of the row in the CSV
        csv_path: Path to CSV file (defaults to blog_info_snapshot.csv in current dir)
        doc_id_override: Optional Google Doc ID to override the one in CSV
        date: Blog post date (defaults to today)
    
    Returns:
        blog_filename if successful, None otherwise
    """
    if csv_path is None:
        csv_path = os.path.join(_current_directory(), 'blog_info_snapshot.csv')
    
    if date is None:
        date = _today_date_str()
    
    # Read CSV and get row
    try:
        df = pd.read_csv(csv_path, index_col=0)
        blog_info_ser = df.iloc[row_index]
    except (FileNotFoundError, IndexError) as e:
        print(f"ERROR: Could not read CSV row {row_index}\n{e}")
        return None
    
    # Determine doc_id
    doc_id = doc_id_override or blog_info_ser.get('doc_id')
    
    if pd.isna(doc_id) or not doc_id:
        print(f"SKIP: Row {row_index} has no doc_id (external blog link)")
        raise ValueError("No doc_id found in spreadsheet row. Please specify a doc_id_override.")
    
    # Connect to Google Drive
    drive = drive_connection()
    
    # 1. Get document name and content
    doc_name = _get_doc_name_from_drive(doc_id, drive)
    doc_content = _get_doc_content_as_markdown(doc_id, drive)
    blog_filename = _create_blog_filename_with_date(doc_name, date)
    
    # 2. Convert to HTML
    html_body = _markdown_to_html(doc_content)
    
    # 3. Build YAML header
    author_name = blog_info_ser.get('author_name', 'Unknown')
    author_role = blog_info_ser.get('author_role', '')
    description = blog_info_ser.get('description', '')
    source = blog_info_ser.get('source', '')

    
    yaml_header = YAML_HEADER.format(
        title=doc_name.title(),
        date=date,
        author_name=author_name,
        author_role=author_role,
        image_path='[IMAGE_PATH]',  # Placeholder, will update after image download
        image_source=source,
        description=description
    )
    
    # 4. Download image if available
    image_link = blog_info_ser.get('image_link')
    if image_link:
        image_path_relative = download_image_and_copy_to_repo(
            image_link, blog_filename=blog_filename, drive=drive
        )
        if image_path_relative:
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
    # example usage: python blog_exporter.py # this will export the blog from the last row of the CSV
    parser = argparse.ArgumentParser(description="Export a blog from CSV row into HTML.")
    parser.add_argument(
        "--row_index", type=int, default=-1, help="Index of the row in blog_info_snapshot.csv"
    )
    parser.add_argument("--csv_path", help="Path to CSV file (default: blog_info_snapshot.csv)")
    parser.add_argument("--doc_id", help="Override doc_id from CSV")
    parser.add_argument("--date", help="Date for blog post (YYYY-MM-DD). Defaults to today.")
    
    args = parser.parse_args()
    export_blog_from_csv_row(args.row_index, args.csv_path, args.doc_id, args.date)
