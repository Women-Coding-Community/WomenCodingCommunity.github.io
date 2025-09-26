"""
    Create a script that will update availability and hours for mentors in preparation for adhoc registration for a specified month
"""
# !/usr/bin/env python

import logging
import sys
import pandas as pd
from ruamel.yaml import YAML

yaml = YAML()
yaml.width = 4096

TYPE_LONG_TERM = "long-term"
TYPE_AD_HOC = "ad-hoc"
TYPE_BOTH = "both"

MONTHS_MAP = {
    4: 'April',
    5: 'May',
    6: 'June',
    7: 'July',
    8: 'August',
    9: 'September',
    10: 'October',
    11: 'November'
}


def get_available_mentor_sort(mentor, current_availability):
    """
        Returns sort value for mentor if:
        - mentor is new (availability still contains full list of months), sort to highest: 500
        - mentor has >3 available hours, sort to highest: 500
        - 3 or less hours, sort: 200
        - mentor is long-term only, sort: 10

        Guide: https://docs.google.com/document/d/1GwlleBNScHCQ3K8rgvYIB3upIr1BylgWjGR2jxwYWtI/edit?tab=t.0
    """

    if len(current_availability) > 1 or mentor.get('hours') > 3:
        return 500
    
    return 200


def get_unavailable_mentor_sort(mentor):
    """
        Returns sort value for mentor if:
        - mentor is ad-hoc only or both but no available hours for the month, sort: 100
        - mentor is long-term only, sort: 10
    """
    if mentor.get("type") == TYPE_LONG_TERM:
        return 10
    
    return 100


def get_availability_update_dict(available_mentors):
    """
       Returns a dictionary mapping mentor to their available hours (from spreadsheet file)
    """
    availability_update_dict = {}

    for _, row in available_mentors.iterrows():
        mentor_name = row['Mentor Name'].strip()
        updated_hours = row['Availability (Hours)']

        # if hours column in spreadhseet is empty, existing hours should be kept
        if pd.isna(updated_hours) or str(updated_hours).strip() == "":
            availability_update_dict[mentor_name] = None
        else:
            availability_update_dict[mentor_name] = updated_hours

    return availability_update_dict


def update_mentor_availability(month, xlsx_file_path, yml_file_path):
    df_available_mentors = pd.read_excel(xlsx_file_path)
    availability_updates = get_availability_update_dict(df_available_mentors)
    
    with open(yml_file_path, 'r') as input_yml:
        mentors = yaml.load(input_yml) or []

    for mentor in mentors:
        yml_name = mentor['name'].strip()

        if yml_name not in availability_updates:
            mentor['sort'] = get_unavailable_mentor_sort(mentor)
            mentor['availability'] = []
            continue 

        current_availability = mentor.get('availability', [])
        logging.info(f"Current availability for {yml_name}: {current_availability}")

        mentor['sort'] = get_available_mentor_sort(mentor, current_availability)
            
        # reset availability to the current month only
        mentor['availability'] = [month]

        # Only update hours if updated hours is None
        updated_hours = availability_updates.get(yml_name)
        if updated_hours is not None:
            mentor['hours'] = availability_updates[yml_name]

    with open(yml_file_path, 'w') as f:
        yaml.default_flow_style = True
        yaml.dump(mentors, f)

    print(f"Mentor availability updated for month {MONTHS_MAP[month]}.")


def run_automation():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    mentors_yml_file_path = "../_data/mentors.yml"

    if len(sys.argv) == 3:
        xlsx_file_path = sys.argv[1]
        month = int(sys.argv[2])

        logging.info("Using values: xlsx: %s, month: %s", xlsx_file_path, month)
    else:
        xlsx_file_path = "samples/adhoc-prep.xlsx"
        month = 11

        logging.info("Default values: xlsx: %s, month: %s", xlsx_file_path, month)

    update_mentor_availability(month, xlsx_file_path, mentors_yml_file_path)


if __name__ == "__main__":
    run_automation()
