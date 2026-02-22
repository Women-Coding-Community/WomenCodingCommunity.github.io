"""
    Create a script that will convert mentor's data from mentors.xlsx to mentors.yml file
"""
# !/usr/bin/env python

import logging
import re
import sys
import textwrap
from enum import Enum

import numpy as np
import pandas as pd
from ruamel.yaml import YAML
from ruamel.yaml.scalarstring import LiteralScalarString
from ruamel.yaml.comments import CommentedSeq

SHEET_NAME = "WCC All Approved Mentors"
TELEGRAM_WEB_SITE = '//t.'
TWITTER_OLD = 'twitter'
TWITTER = 'x.com'
SOCIAL_MEDIA = ['linkedin', 'github', 'medium', 'youtube', 'instagram', TELEGRAM_WEB_SITE, 'meetup', 'slack',
                'facebook', TWITTER_OLD, TWITTER]
WEBSITE = 'website'
TELEGRAM = 'telegram'

# Indexes for creating yaml sequences of data
AREAS_START_INDEX = 13
AREAS_END_INDEX = 17
FOCUS_START_INDEX = 18
FOCUS_END_INDEX = 22
PROG_LANG_START_INDEX = 23
PROG_LANG_END_INDEX = 27

type_ad_hoc = ("ad-hoc", "ad hoc")
type_long_term = ("long-term", "long term")
TYPE_BOTH = "both"
IMAGE_FILE_PATH = "assets/images/mentors"
IMAGE_SUFFIX = ".jpeg"

# Mentorship cycle periods
LONG_TERM_REG_PERIOD = "long-term" # long-term registrations period only
DEFAULT_PERIOD = "default" # rest of the cycle, ad-hoc periods


class WriteMode(Enum):
    # Create new a file
    WRITE = "w"
    # Append in existent yml file
    APPEND = "a"


def fallback_link(link):
    """
        Use "webpage" keyword as fallback in case of unknown link.
     """
    return {WEBSITE: link}


def strings_to_list(*string_args):
    """
    Clean strings and create to list
    """
    data_str = ""

    for item in string_args:
        if not pd.isna(item) and len(item):
            data_str += item + " "

    return data_str.split()


def get_social_media_links(*links_args):
    """
    Prepare mentor's social media links for yaml network sequence.
    """
    network_list = []
    social_media_links_list = strings_to_list(*links_args)

    for link in social_media_links_list:
        found = 0
        if any(link.startswith(prefix) for prefix in ["http://", "https://", "www."]):
            for name in SOCIAL_MEDIA:
                if link.find(name) != -1:
                    if name == TELEGRAM_WEB_SITE:
                        network_list.append({TELEGRAM: link})
                    else:
                        if name != TWITTER_OLD and name != TWITTER:
                            network_list.append({name: link})
                    found = 1
                    break
            if found == 0:
                    network_list.append(fallback_link(link))

    return network_list


def get_yaml_block_sequence(mentor_data, start_index, end_index):
    """
    Yaml block sequence is presented as a list of entries marked with
    dash and space (“- ”). 
    """
    block_sequence_list = []
    for entry in range(start_index, end_index + 1):
        if not pd.isna(mentor_data.iloc[entry]) and len(mentor_data.iloc[entry].strip()):
            block_sequence_list.append(str(mentor_data.iloc[entry]).rstrip())

    return block_sequence_list


def extract_numbers_from_string(text_arg, get_max_value=True):
    """
    Extract numbers and convert them to integers.
    """
    if pd.isna(text_arg):
        text_arg = 0

    if isinstance(text_arg, str):
        digits = [int(num) for num in re.findall(r"\d+", text_arg)]
        if digits:
            if get_max_value:
                return max(digits)
            return digits

    return int(text_arg)


def get_multiline_string(long_text_arg):
    """
    Save strings as yaml multiline strings.
    Use literal block scalar style to keep newlines (yaml sign: '|-').
    """
    multiline_str = ""
    if not pd.isna(long_text_arg):
        multiline_str = LiteralScalarString(textwrap.dedent(long_text_arg))
    return multiline_str

def is_available_for_long_term(mentorship_type):
    return mentorship_type == type_long_term[0] or mentorship_type == TYPE_BOTH

def is_available_for_ad_hoc(mentorship_type):
    return mentorship_type == type_ad_hoc[0] or mentorship_type == TYPE_BOTH

def sort_for_long_term_reg(num_mentee):
    """
    Return sort value for mentors available for long-term, based on number of mentees they can take.
    Applies only during long-term registration period.
    if no mentees, sort to 10; if num_mentees is 1, sort to 100; 2, sort to 200; if >2, sort to highest 500
    """
    
    mentee_sort_map = {
        0: 10, 
        1: 100, 
        2: 200
    }
    return mentee_sort_map.get(num_mentee, 500)


def get_sort(mentorship_type, current_period, num_mentee):
    """
    Get sort value for a new mentor
    Rules: https://docs.google.com/document/d/1GwlleBNScHCQ3K8rgvYIB3upIr1BylgWjGR2jxwYWtI/edit?usp=sharing
    """

    if current_period == LONG_TERM_REG_PERIOD and is_available_for_long_term(mentorship_type):
        return sort_for_long_term_reg(num_mentee)
    
    if current_period == DEFAULT_PERIOD and is_available_for_ad_hoc(mentorship_type):
        return 500

    # else the mentor is not available for any periods
    return 10

def get_mentorship_type(mentorship_type_str):
    """
    Returns ad-hoc, long-term, both or NOT_FOUND str
    """
    mentorship_type = mentorship_type_str.lower()

    result = "NOT_FOUND"

    if any(item in mentorship_type for item in type_ad_hoc):
        result = type_ad_hoc[0]
    elif any(item in mentorship_type for item in type_long_term):
        result = type_long_term[0]
    elif TYPE_BOTH in mentorship_type:
        result = TYPE_BOTH

    return result

def add_availability(months_str):
    """
    Convert a comma-separated string of month names to a list of month numbers.
    If the string is empty, return an empty list.
    """

    month_map = {
        'april': 4,
        'may': 5,
        'june': 6,
        'july': 7,
        'august': 8,
        'september': 9,
        'october': 10,
        'november': 11
    }

    if not isinstance(months_str, str):
        months_str = str(months_str)

    if not months_str.strip():
        return []

    months_list = [month.strip().lower() for month in months_str.split(',')]
    months_numbers = [month_map[month] for month in months_list if month in month_map]

    availability_seq = CommentedSeq(months_numbers)
    availability_seq.fa.set_flow_style()

    return availability_seq

def update_yml_file_formatting(s):
    """
    Insert new line before each new mentor.
    Replace yaml string formatting indicator '|-' with '|'
    """
    updated_string = s.replace('- name: ', '\n- name: ').replace('|-', '|')
    return updated_string


def write_yml_file(file_path, mentors_data, mode: WriteMode):
    """
    Create new or append to mentors.yml file
    :mentors_data: list of dictionaries
    :mode: write or append
    """
    with open(file_path, str(mode.value), encoding="utf-8") as output_yml:
        yaml = YAML()

        # Display yaml content in block style (not inline)
        yaml.default_flow_style = False

        # TODO: Currently do not use indent() - discuss with Adriana
        # yaml.indent(mapping=2, sequence=4, offset=2)

        yaml.dump(mentors_data, output_yml, transform=update_yml_file_formatting)

    logging.info(f"File: {file_path} is successfully written.")


def read_yml_file(file_path):
    """
    Read yml file
    """
    with open(file_path, 'r', encoding="utf-8") as input_yml:
        yaml = YAML(typ='safe')
        yml_dict = yaml.load(input_yml) or {}
        logging.info(f"File: {file_path} is successfully read.")

    return yml_dict

def get_num_mentee_from_row(mentor_row):
    """
    Gets the 'num_mentee' value for a new mentor from mentor_row, or use a default value if invalid.
    """
    val = mentor_row.iloc[31]

    return int(val) if pd.notna(val) else 0

def get_mentor_position(mentor_row):
    """
    Returns formatted value for mentor role and company
    """
    if not pd.isna(mentor_row.iloc[5]):
        return f"{mentor_row.iloc[4].strip()}, {mentor_row.iloc[5].strip()}"
    else:
        return mentor_row.iloc[4].strip()


def xlsx_to_yaml_parser(mentor_row,
                        mentor_index,
                        current_period,
                        mentor_disabled=False,
                        mentor_sort=0,
                        mentor_matched=False,
                        num_mentee=0):
    """
    Prepare mentor's excel data for yaml format
    """
    areas = get_yaml_block_sequence(mentor_row, AREAS_START_INDEX, AREAS_END_INDEX)
    focus = get_yaml_block_sequence(mentor_row, FOCUS_START_INDEX, FOCUS_END_INDEX)
    programming_languages = get_yaml_block_sequence(mentor_row, PROG_LANG_START_INDEX, PROG_LANG_END_INDEX)

    mentor_image = f"{IMAGE_FILE_PATH}/{mentor_row.iloc[0].strip().lower().replace(' ', '_')}{IMAGE_SUFFIX}"
    # Format mentor role and company
    mentor_position = get_mentor_position(mentor_row)

    mentor_type = get_mentorship_type(mentor_row.iloc[6])

    # If mentor is new i.e mentor_sort is 0 (from default input), get the correct num_mentees and sort values
    if mentor_sort == 0:
        num_mentee = get_num_mentee_from_row(mentor_row)
        mentor_sort = get_sort(mentor_type, current_period, num_mentee)

    mentor = {
        'name': mentor_row.iloc[0].strip(),
        'disabled': mentor_disabled,
        'matched': mentor_matched,
        'sort': mentor_sort,
        'num_mentee': num_mentee,
        'hours': extract_numbers_from_string(mentor_row.iloc[30]),
        'type': mentor_type,
        'index': mentor_index,
        'location': mentor_row.iloc[3],
        'position': mentor_position,
        'bio': get_multiline_string(mentor_row.iloc[10]),
        'image': get_multiline_string(mentor_image),
        'languages': mentor_row.iloc[8],
        'availability': add_availability(mentor_row.iloc[7]),
        'skills': {
            'experience': mentor_row.iloc[9],
            'years': extract_numbers_from_string(mentor_row.iloc[9]),
            'mentee': get_multiline_string(mentor_row.iloc[28]),
            'areas': areas,
            'languages': ', '.join(programming_languages),
            'focus': focus,
            'extra': get_multiline_string(mentor_row.iloc[11])
        },
        'network': get_social_media_links(mentor_row.iloc[32], mentor_row.iloc[33]),
    }
    return mentor


def get_yml_data(yml_file_path):
    """
    Get data from mentors.yml.
    Return dataframe with name, index, sort, disabled, matched and num_mentee values.
    """
    yml_dict = read_yml_file(yml_file_path)

    logging.info(f"Mentors yml total: {len(yml_dict)}")

    yml_data = []

    for mentor in yml_dict:
        if 'matched' in mentor:
            matched = mentor['matched']
        else:
            matched = False

        if 'num_mentee' in mentor:
            num_mentee = mentor['num_mentee']
        else:
            num_mentee = 0

        yml_data.append([mentor['name'].strip().lower(),
                        mentor['index'],
                        mentor['disabled'],
                        mentor['sort'],
                        matched,
                        num_mentee])

    df_yml_data = pd.DataFrame(yml_data,
                            columns=['Name', 'Index', 'Disabled', 'Sort', 'Matched', 'Num_mentee'])
    return df_yml_data


def get_all_mentors_in_yml_format(yml_file_path, xlsx_file_path, current_period, skip_rows=0):
    """
    Read all mentors from Excel sheet:
     - if mentor is in current mentors.yml, use existing values for index, disabled, sort, matched and num_mentee.
     - if mentor is new, continue indexing from the largest index from current mentors.yml
    """
    df_mentors = pd.read_excel(xlsx_file_path, sheet_name=SHEET_NAME, skiprows=skip_rows)

    logging.info(f"Excel read {len(df_mentors)} mentors")

    # Get current mentors' data (name, index, disabled, sort) from mentors.yml
    df_yml = get_yml_data(yml_file_path)

    new_index = 1
    if not df_yml.empty:
        new_index = df_yml['Index'].max().item() + 1

    mentors = []

    for row in range(0, len(df_mentors)):
        mentor_name = df_mentors.iloc[row].values[0].strip().lower()

        df_yml_row = df_yml.loc[df_yml.Name == mentor_name]

        if not df_yml_row.empty:
            mentor = xlsx_to_yaml_parser(df_mentors.iloc[row],
                                        df_yml_row['Index'].item(),
                                        current_period,
                                        df_yml_row['Disabled'].item(),
                                        df_yml_row['Sort'].item(),
                                        df_yml_row['Matched'].item(),
                                        df_yml_row['Num_mentee'].item())
            logging.info(f"For {mentor_name} use index, disabled and sort from mentors.yml file")
        else:
            mentor = xlsx_to_yaml_parser(df_mentors.iloc[row],
                                        new_index,
                                        current_period)
            new_index += 1
        mentors.append(mentor)

    logging.info(f"Added {len(mentors)} mentors to the mentors.yml file")

    return mentors


def get_new_mentors_in_yml_format(yml_file_path, xlsx_file_path, current_period, skip_rows=1):
    """
    Read just new mentors from Excel sheet:
     - start reading xlsx Mentors from the row 1 (from the date 03/04/2024)
     - find diff. between current mentors.yml and xlsx table
    """
    df_mentors = pd.read_excel(xlsx_file_path, sheet_name=SHEET_NAME, skiprows=skip_rows)

    logging.info(f"Excel mentors: {len(df_mentors)}")

    # Get current mentors' data (name, index, disabled, sort, matched, num_mentee) from mentors.yml
    df_yml = get_yml_data(yml_file_path)

    mentors = []

    if not df_yml.empty:
        new_index = df_yml['Index'].max().item() + 1

        for row in range(0, len(df_mentors)):
            if df_mentors.iloc[row].isnull().all():
                break

            mentor_name = df_mentors.iloc[row].values[0].strip().lower()

            if df_yml.loc[df_yml.Name == mentor_name].empty:
                mentor = xlsx_to_yaml_parser(df_mentors.iloc[row], new_index, current_period)
                new_index += 1
                mentors.append(mentor)

        logging.info(f"Added {len(mentors)} mentors to the mentors.yml file")
    else:
        mentors = get_all_mentors_in_yml_format(yml_file_path, xlsx_file_path, skip_rows)

    return mentors


def run_automation():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    if len(sys.argv) == 6:
        xlsx_file_path = sys.argv[1]
        yml_file_path = sys.argv[2]
        current_period = sys.argv[3]
        mode = WriteMode(sys.argv[4])
        skip_rows = int(sys.argv[5])

        logging.info("Params: xlsx: %s yml: %s current_period: %s mode: %s skip_rows: %s", xlsx_file_path, yml_file_path, current_period, mode, skip_rows)
    else:
        xlsx_file_path = "samples/mentors.xlsx"
        yml_file_path = "samples/mentors.yml"
        current_period = "default"
        mode = WriteMode.APPEND
        skip_rows = 0

        logging.info("Default values: xlsx: %s yml:: %s current_period: %s mode: %s", xlsx_file_path, yml_file_path, current_period, mode)

    if mode == WriteMode.APPEND:
        logging.info("Appending option selected.")

        list_of_mentors = get_new_mentors_in_yml_format(yml_file_path, xlsx_file_path, current_period, skip_rows=skip_rows)

        logging.info("New Mentors size: %d", len(list_of_mentors))

        if list_of_mentors:
            write_yml_file(yml_file_path, list_of_mentors, WriteMode.APPEND)

    elif mode == WriteMode.WRITE:
        logging.info("Recreate yml - Write option selected.")

        list_of_mentors = get_all_mentors_in_yml_format(yml_file_path, xlsx_file_path, current_period, skip_rows=skip_rows)
        write_yml_file(yml_file_path, list_of_mentors, WriteMode.WRITE)


if __name__ == "__main__":
    run_automation()
