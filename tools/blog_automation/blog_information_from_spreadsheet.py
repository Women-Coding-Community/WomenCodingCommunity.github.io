import re
import pandas as pd

SPREADSHEET_ID = '1Pje2qOn23OgtAyhjqKwQFYcaEAE3gAy5f3T_5LCgA2o'

def _extract_doc_id_from_url(url):
    """Extract the document ID from a Google Docs URL."""
    match = re.search(r'/document/d/([a-zA-Z0-9-_]+)', url)
    if match:
        return match.group(1)
    else:
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
    return formatted_df

def dataframe_of_blog_spreadsheet_info(spreadsheet_id=SPREADSHEET_ID):
    import gspread
    import pandas as pd

    gc = gspread.service_account(filename="service_account_key.json")
    sh = gc.open_by_key(spreadsheet_id)
    worksheet = sh.worksheet("Form Responses 1")
    data = worksheet.get_all_records()
    df = pd.DataFrame(data)
    return df

if __name__=='__main__':
    df = dataframe_of_blog_spreadsheet_info()
    formatted_df = df.pipe(_extract_and_rename_relevant_fields)
    formatted_df.to_csv('blog_info_snapshot.csv')






