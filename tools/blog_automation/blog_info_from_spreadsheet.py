import re
import pandas as pd

SPREADSHEET_ID = '1Pje2qOn23OgtAyhjqKwQFYcaEAE3gAy5f3T_5LCgA2o'
WORKSHEET_NAME = 'Form Responses 1'

# Spreadsheet columns that drive the pipeline (maintained by the review team):
#   REVIEWED_COLUMN  -> reviewer ticks TRUE once a blog is reviewed & approved.
#   PUBLISHED_COLUMN -> TRUE once the blog is live on the site.
# A blog is exported when REVIEWED_COLUMN is TRUE and PUBLISHED_COLUMN is not.
REVIEWED_COLUMN = 'isReviewedandApproved'
PUBLISHED_COLUMN = 'isPublished'

def _extract_doc_id_from_url(url):
    """Extract the Google document/file ID from a Drive or Docs URL.

    Handles the formats the submission form produces, e.g.
      https://docs.google.com/document/d/<ID>/edit
      https://drive.google.com/open?id=<ID>
      https://drive.google.com/file/d/<ID>/view
    """
    if not isinstance(url, str):
        return None
    match = re.search(r'(?:/d/|[?&]id=)([a-zA-Z0-9-_]+)', url)
    if match:
        return match.group(1)
    return None

def _extract_and_rename_relevant_fields(df):
    formatted_df = pd.DataFrame({})
    formatted_df['url'] = df['Upload your writing draft for review']
    formatted_df['doc_id'] = formatted_df['url'].apply(_extract_doc_id_from_url)
    formatted_df['author_name'] = df['What is your full name? ']
    formatted_df['author_role'] = df['What is your position / company you are working at / associated with? ']
    formatted_df['description'] = df['Please provide a short description of your writing idea / blog post? ']
    formatted_df['source'] = df[
            'Please provide a source of how you obtained/created the infographic/photo/picture used.'
        ]
    formatted_df['image_link'] = df['Submit your blog cover image']
    # Review/publish tracking columns; default to blank if not present yet.
    formatted_df['is_reviewed_and_approved'] = df[REVIEWED_COLUMN] if REVIEWED_COLUMN in df.columns else ''
    formatted_df['is_published'] = df[PUBLISHED_COLUMN] if PUBLISHED_COLUMN in df.columns else ''
    return formatted_df

def get_worksheet(spreadsheet_id=SPREADSHEET_ID):
    """Open the submissions worksheet with the service account (read + write)."""
    import gspread

    gc = gspread.service_account(filename="service_account_key.json")
    return gc.open_by_key(spreadsheet_id).worksheet(WORKSHEET_NAME)

def dataframe_from_worksheet(worksheet):
    """Build a DataFrame from a worksheet's raw cell values.

    Uses raw values rather than get_all_records(): the form sheet has duplicate
    (blank) header cells, which get_all_records() rejects. pandas tolerates
    duplicate column names, and we only ever select uniquely-named columns.
    """
    values = worksheet.get_all_values()
    header, rows = values[0], values[1:]
    return pd.DataFrame(rows, columns=header)

def dataframe_of_blog_spreadsheet_info(spreadsheet_id=SPREADSHEET_ID):
    return dataframe_from_worksheet(get_worksheet(spreadsheet_id))

def mark_row_published(worksheet, data_row_index):
    """Set the isPublished cell to TRUE for a data row (0-based, header excluded).

    Requires the service account to have edit access to the spreadsheet.
    """
    header = worksheet.row_values(1)
    col = header.index(PUBLISHED_COLUMN) + 1   # gspread is 1-based
    worksheet.update_cell(data_row_index + 2, col, 'TRUE')  # +2: header row + 1-based

if __name__ == '__main__':
    # Quick connectivity check: print the columns and review/publish counts.
    df = dataframe_of_blog_spreadsheet_info()
    print(f"{len(df)} rows; columns: {list(df.columns)}")






