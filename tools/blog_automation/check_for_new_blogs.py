import os
import pandas as pd
from tools.blog_automation.blog_info_from_spreadsheet import dataframe_of_blog_spreadsheet_info

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def load_previous_blog_info():
    """Load the previously saved blog info snapshot."""
    try:
        df = pd.read_csv(os.path.join(SCRIPT_DIR, 'blog_info_snapshot.csv'), index_col=0)
        return df
    except FileNotFoundError:
        print("ERROR: blog_info_snapshot.csv not found.")
        print("Please run: python blog_information_from_spreadsheet.py save_blog_info_to_csv()")
        return None

def check_and_update_blogs():
    """
    Check for new blogs by comparing row counts with the snapshot.
    Outputs GitHub Actions variables for has_new_rows and new_row_indices.
    
    Returns:
        tuple: (has_new_rows: bool, new_row_indices: list)
    """
    df_previous = load_previous_blog_info()
    if df_previous is None:
        return False, []
    
    df_current = dataframe_of_blog_spreadsheet_info()
    
    count_previous = df_previous.shape[0]
    count_current = df_current.shape[0]
    
    new_row_indices = []
    
    if count_current > count_previous:
        # New rows added
        new_blog_count = count_current - count_previous
        print(f"Found {new_blog_count} new blog(s)")
        
        # Calculate the indices of new rows (0-indexed in the CSV, but the new rows start from count_previous)
        new_row_indices = list(range(count_previous, count_current))
        print(f"New row indices: {new_row_indices}")
        has_new_rows = True
    elif count_current < count_previous:
        print("WARNING: Current count is less than previous count. This is unexpected.")
        has_new_rows = False
    else:
        print("No new blogs found.")
        has_new_rows = False
    
    # Check if any existing rows have changed
    if not (df_previous.eq(df_current[:count_previous])).all().all():
        for i, (idx, row) in enumerate(df_previous.iterrows()):
            if i < len(df_current) and not row.equals(df_current.iloc[i]):
                print(f"INFO: Row {i} has changed (not re-processing)")
    
    # Update snapshot for next run
    df_current.to_csv(os.path.join(SCRIPT_DIR, 'blog_info_snapshot.csv'))
    
    return has_new_rows, new_row_indices


if __name__ == '__main__':
    has_new_rows, new_row_indices = check_and_update_blogs()
    
    # Output for GitHub Actions
    # Set has_new_rows output
    print(f"::set-output name=has_new_rows::{str(has_new_rows).lower()}")
    
    # Set new_row_indices output (space-separated)
    indices_str = ' '.join(map(str, new_row_indices))
    print(f"::set-output name=new_row_indices::{indices_str}")
