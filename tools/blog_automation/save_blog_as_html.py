import shutil
from google.oauth2 import service_account
from googleapiclient.discovery import build
import os
import markdown
import argparse
from pathlib import Path
from googleapiclient.errors import HttpError
import datetime as dt
import pandas as pd
import re

# --- Configuration ---
SERVICE_ACCOUNT_FILE = 'service_account_key.json'
SPREADSHEET_ID = '1Pje2qOn23OgtAyhjqKwQFYcaEAE3gAy5f3T_5LCgA2o'
YAML_HEADER = '''---
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

# TODO: Use information from spreadsheet with optional doc_ID param

def _current_directory():
    return Path(__file__).resolve().parent

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

DRIVE = drive_connection()

def get_blog_info_from_spreadsheet(spreadsheet_id=SPREADSHEET_ID):
    import gspread
    import pandas as pd

    # 1) Authenticate using the service account JSON
    gc = gspread.service_account(filename="service_account_key.json")

    # 2) Open the spreadsheet by its ID
    spreadsheet_id = SPREADSHEET_ID
    sh = gc.open_by_key(spreadsheet_id)

    # 3) Select a worksheet/tab (by gid or title)
    worksheet = sh.worksheet("Form Responses 1")

    # 4) Get data
    data = worksheet.get_all_records()

    # 5) Convert to a pandas DataFrame
    df = pd.DataFrame(data)
    return df

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

def _update_yaml_header_with_spreadsheet_info(yaml_header):
    spreadsheet_info = get_blog_info_from_spreadsheet(drive=DRIVE).iloc[-1].to_dict()
    try:
        author_name = spreadsheet_info['What is your full name? ']
        author_role = spreadsheet_info[
            'What is your position / company you are working at / associated with? '
        ]
        description = spreadsheet_info['Please provide a short description of your writing idea / blog post? ']
        source = spreadsheet_info[
            'Please provide a source of how you obtained/created the infographic/photo/picture used.'
        ]
        yaml_header = yaml_header.replace('[AUTHOR]', author_name)
        yaml_header = yaml_header.replace('[AUTHOR ROLE]', author_role)
        yaml_header = yaml_header.replace('[DESCRIPTION]', description)
        yaml_header = yaml_header.replace('[SOURCE]', source)
        return yaml_header
    except KeyError as error:
        print(f'Unable to find relevant spreadsheet field. Please check the spreadsheet carefully.\n{error}')

def export_blog_as_html(document_id, date=None, drive=DRIVE):
    if date is None:
        date = _today_date_str()

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
    yaml_header = _update_yaml_header_with_spreadsheet_info(yaml_header)

    final_html = yaml_header + '\n' + html_body

    posts_dir = _posts_directory()
    filename = f"{posts_dir}/{blog_filename}.html"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(final_html)

    print(f"Saved HTML to: {filename}")
    return blog_filename

def download_blog_image(spreadsheet_info):
    blog_image_drive_link = spreadsheet_info['Submit your blog cover image']
    file_id = re.search(r'drive\.google\.com/file/d/([^/]+)/', blog_image_drive_link).group(1)
    # Download the image file
    try:
        request = DRIVE.files().get_media(fileId=file_id)
        image_data = request.execute()
        # Save the image locally
        image_filename = f"blog_image_{file_id}.jpg"
        with open(image_filename, 'wb') as img_file:
            img_file.write(image_data)
        return image_filename
    except HttpError as error:
        print(f"Error downloading image: {error}")
        return None
    
def copy_image_to_blog_assets(image_filename, blog_filename):
    assets_dir = Path(__file__).resolve().parent.parent.parent / 'assets' / 'images' / 'blog'
    assets_dir.mkdir(parents=True, exist_ok=True)
    date_prefix = blog_filename.split('-')[0]
    new_image_filename = f"{date_prefix}-{image_filename}"
    new_image_path = assets_dir / new_image_filename
    shutil.copy(image_filename, new_image_path)
    return f"/assets/images/blog/{new_image_filename}"

def export_blog_with_image(document_id):
    spreadsheet_info = get_blog_info_from_spreadsheet(drive=DRIVE)
    blog_filename = export_blog_as_html(document_id, spreadsheet_info)
    image_filename = download_blog_image(spreadsheet_info)
    copy_image_to_blog_assets(image_filename, blog_filename)

if __name__ == "__main__":
    # To run script: `python export_blog.py <DOC_ID> --date <DATE>`
    parser = argparse.ArgumentParser(description="Export a Google Doc as HTML with custom formatting.")
    parser.add_argument("doc_id", help="The Google Doc ID to export.")
    parser.add_argument("--date", help="Date for the blog post (YYYY-MM-DD). If not provided, uses today.", default=None)
    args = parser.parse_args()
    export_blog_as_html(args.doc_id, args.date)
