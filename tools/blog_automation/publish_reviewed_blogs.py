"""Export every blog that has been reviewed but not yet published.

This is the single entry point the GitHub Action runs. The Google Sheet is the
only source of truth; there is no local snapshot. On each run it:

  1. Reads the Form Responses sheet via the service account.
  2. Selects rows where ``isReviewedandApproved`` is TRUE and ``isPublished`` is
     not TRUE (i.e. approved but not yet on the site).
  3. Exports each selected blog (Doc -> HTML post + cover image).
  4. Writes ``isPublished = TRUE`` back to the sheet for each exported row, so it
     is never exported again.

The workflow then opens a PR with the new ``_posts/`` files and images for a
human to review before merging.

Requirements:
  - The service account must have **edit** access to the spreadsheet (step 4
    writes back to it).
  - Must be run from this directory (the service account key and the Jekyll
    ``_posts`` folder are resolved relative to it).
"""
import pandas as pd

from blog_info_from_spreadsheet import (
    get_worksheet,
    dataframe_from_worksheet,
    _extract_and_rename_relevant_fields,
    mark_row_published,
)
from blog_exporter import export_blog


def _is_true(value):
    """True for the sheet's ``TRUE``/truthy cell values (case-insensitive)."""
    return str(value).strip().lower() in {'true', 'yes', '1'}


def _select_rows_to_publish(df):
    """Indices of rows that are approved, not yet published, and have a doc_id."""
    to_publish = []
    for i, (_, row) in enumerate(df.iterrows()):
        if not _is_true(row.get('is_reviewed_and_approved')):
            continue
        if _is_true(row.get('is_published')):
            continue
        if pd.isna(row.get('doc_id')) or not str(row.get('doc_id')).strip():
            print(f"SKIP row {i}: approved but has no doc_id (external blog link).")
            continue
        to_publish.append(i)
    return to_publish


def main():
    worksheet = get_worksheet()
    df = _extract_and_rename_relevant_fields(
        dataframe_from_worksheet(worksheet)
    ).reset_index(drop=True)

    to_publish = _select_rows_to_publish(df)
    if not to_publish:
        print("No reviewed, unpublished blogs to export.")
        return

    print(f"Exporting {len(to_publish)} reviewed blog(s): rows {to_publish}")
    for i in to_publish:
        row = df.iloc[i]
        try:
            blog_filename = export_blog(row)
        except Exception as error:  # keep going so one bad row can't block the rest
            print(f"ERROR exporting row {i} ({row.get('author_name')!r}): {error}")
            continue
        if blog_filename:
            mark_row_published(worksheet, i)
            print(f"Marked row {i} as published in the sheet.")


if __name__ == '__main__':
    main()
