from google.oauth2 import service_account
from googleapiclient.discovery import build
import os
import markdown
import argparse
from pathlib import Path
from googleapiclient.errors import HttpError
import datetime as dt

# --- Configuration ---
SERVICE_ACCOUNT_FILE = 'service_account_key.json'
YAML_HEADER = '''
---
layout: post
title: [TITLE]
date: [DATE]
author_name: [AUTHOR]
author_role: [AUTHOR ROLE]
image: [IMG PATH]
image_source: [IMG SOURCE (optional)]
description: [BLOG DESCRIPTION]
category: [CATEGORY]
---
'''

def _current_directory():
    return Path(__file__).resolve().parent

def _posts_directory():
    # Path to the directory where the script itself is located
    script_dir = _current_directory()

    # Construct the path relative to the script’s location
    posts_dir = (script_dir / "../../_posts").resolve()

    return posts_dir

def _today_date_str():
    return dt.date.today().isoformat()

def _create_blog_filename_with_date(doc_name, date_str):
    formatted_blog_title = doc_name.lower().replace(' ', '-').strip()
    filename = f"{date_str}-{formatted_blog_title}"
    return filename

def export_blog_as_html(document_id, date=None):
    if date is None:
        date = _today_date_str()
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

    try:
        # 1. Get document name from Drive
        doc_metadata = drive.files().get(fileId=document_id, fields='name').execute()
        doc_name = doc_metadata.get('name', 'exported_blog')
        blog_filename = _create_blog_filename_with_date(doc_name, date)

        # 2. Export as Markdown
        request = drive.files().export_media(
            fileId=document_id,
            mimeType='text/markdown'
        )
        md_bytes = request.execute()
    except HttpError as error:
        if error.resp.status == 404:
            raise FileNotFoundError(f"Document ID '{document_id}' not found.") from error
        else:
            raise

    # 3. Convert Markdown to HTML and save to local file
    import re
    html = markdown.markdown(md_bytes.decode('utf-8'))
    # Remove <strong> tags from inside heading tags (e.g. <h2><strong>Heading</strong></h2> -> <h2>Heading</h2>)
    html = re.sub(r'<h(\d)><strong>(.+?)</strong></h\1>', r'<h\1>\2</h\1>', html)

    # Remove the first heading if present (e.g. <h1>...</h1> or <h2>...</h2> at the start)
    html = re.sub(r'^<h[1-6]>.*?</h[1-6]>\s*', '', html, flags=re.DOTALL)

    # Wrap the body in <div class="text-justify">
    html_body = f'<div class="text-justify">\n{html}\n</div>'

    # YAML front matter
    yaml_header = YAML_HEADER.replace('[TITLE]', doc_name.title()).replace('[DATE]', date)

    final_html = yaml_header + '\n' + html_body

    posts_dir = _posts_directory()
    filename = f"{posts_dir}/{blog_filename}.html"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(final_html)

    print(f"Saved HTML to: {filename}")

if __name__ == "__main__":
    # To run script: `python export_blog.py <DOC_ID> --date <DATE>`
    parser = argparse.ArgumentParser(description="Export a Google Doc as HTML with custom formatting.")
    parser.add_argument("doc_id", help="The Google Doc ID to export.")
    parser.add_argument("--date", help="Date for the blog post (YYYY-MM-DD). If not provided, uses today.", default=None)
    args = parser.parse_args()
    export_blog_as_html(args.doc_id, args.date)
