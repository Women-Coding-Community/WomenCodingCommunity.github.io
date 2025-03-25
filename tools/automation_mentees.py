"""
    A script saves mentee's data in the xlsx file for the specific mentor.
"""
# !/usr/bin/env python

import logging
import os
import sys
import re
import pandas as pd

SHEET_NAME = "Revised Mentees"
COLUMN_MENTORS_WITH_DESCRIPTION_INDEX = 21
FILE_NAME_LONG_MENTORSHIP_PREFIX = "WWC_long_term_"

def write_xlsx_files(mentor_dict, df_columns, mentor_xlsx_file_path):
    # Iterate through the mentor dictionary to create separate Excel files
    for mentor_name, mentee_data in mentor_dict.items():
        # Create a DataFrame for the mentee data
        mentor_df = pd.DataFrame(mentee_data, columns=df_columns)

        # Generate the file name using the mentor's name
        file_name = f"{FILE_NAME_LONG_MENTORSHIP_PREFIX+mentor_name.replace(' ', '_')}.xlsx"
        file_path = os.path.join(mentor_xlsx_file_path, file_name)

        # Save the DataFrame to an Excel file
        mentor_df.to_excel(file_path, index=False)

        logging.info(f"Excel file created for mentor: {mentor_name} -> {file_name}")

def create_mentor_files_with_mentees(mentee_xlsx_file_path, mentor_xlsx_sheet, mentor_xlsx_file_path):
    pattern_mentor_name = r'\d+\.\s*([A-Za-z]+(?:\s+[A-Za-z]+)*)\s*-'
    pattern_mentor_descr = r'-\s*(.*?)(?=\n\d+\.|\Z)'

    df_mentees = pd.read_excel(mentee_xlsx_file_path, sheet_name=mentor_xlsx_sheet)

    mentor_dict = {}

    for _, row in df_mentees.iterrows():
        if row.isnull().all() or (not row.isnull().iloc[0] and row.iloc[1:].isnull().all()):
            continue

        # Access the value of the specific column (index 21) for each row
        column_value = row.iloc[COLUMN_MENTORS_WITH_DESCRIPTION_INDEX]

        for value in column_value.splitlines():
            match_mentor_name = re.search(pattern_mentor_name, value)
            match_description = re.search(pattern_mentor_descr, value)

            if match_mentor_name:
                mentor_name = match_mentor_name.group(1)
                mentor_description = match_description.group(1) if match_description else ""

                row[df_mentees.columns[COLUMN_MENTORS_WITH_DESCRIPTION_INDEX]] = mentor_description

                # Create a dictionary with mentors as keys and lists of lists as values
                if mentor_name not in mentor_dict:
                    mentor_dict[mentor_name] = []

                # Add the current row's data as a list to the mentor's list of lists
                mentor_dict[mentor_name].append(row.tolist())

    write_xlsx_files(mentor_dict, df_mentees.columns, mentor_xlsx_file_path)

def run_automation():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    if len(sys.argv) == 3:
        mentee_xlsx_file_path = sys.argv[1]
        mentor_xlsx_sheet = sys.argv[2]
        mentor_xlsx_file_path = sys.argv[3]
        logging.info("Params: mentee_xlsx: %s mentee_sheet %s mentor_xlsx: %s", mentee_xlsx_file_path, mentor_xlsx_sheet, mentor_xlsx_file_path)
    else:
        mentee_xlsx_file_path = "tools/samples/mentees.xlsx"
        mentor_xlsx_sheet = SHEET_NAME
        mentor_xlsx_file_path = os.getcwd()
        logging.info("Default values: mentee_xlsx: %s mentor_xlsx: %s", mentee_xlsx_file_path, mentor_xlsx_file_path)

    create_mentor_files_with_mentees(mentee_xlsx_file_path, mentor_xlsx_sheet, mentor_xlsx_file_path)

if __name__ == "__main__":
    run_automation()