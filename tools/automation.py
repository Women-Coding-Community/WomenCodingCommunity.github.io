"""
    Create a script that will convert mentor's data from mentors.xlsx to mentors.yml file
"""
# !/usr/bin/env python

import logging
import re
import sys
import textwrap
from enum import Enum

import pandas as pd
from ruamel.yaml import YAML
from ruamel.yaml.scalarstring import LiteralScalarString

import yml_utils

SHEET_NAME = "Form Responses 1"
TELEGRAM_WEB_SITE = '//t.'
SOCIAL_MEDIA = ['linkedin', 'twitter', 'github', 'medium', 'youtube', 'instagram', TELEGRAM_WEB_SITE, 'meetup', 'slack',
                'facebook']
WEBSITE = 'website'
TELEGRAM = 'telegram'

# Indexes for creating yaml sequences of data
AREAS_START_INDEX = 13
AREAS_END_INDEX = 17
FOCUS_START_INDEX = 18
FOCUS_END_INDEX = 22
PROG_LANG_START_INDEX = 23
PROG_LANG_END_INDEX = 27

TYPE_AD_HOC = "ad hoc"
TYPE_LONG_TERM = "long-term"
TYPE_BOTH = "both"
IMAGE_FILE_PATH = "assets/images/mentors"
IMAGE_SUFFIX = ".jpeg"


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
        for name in SOCIAL_MEDIA:
            if link.find(name) != -1:
                if name == TELEGRAM_WEB_SITE:
                    network_list.append({TELEGRAM: link})
                else:
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
    # TODO: If the field hours in xlsx is NAN, what should be the default: 0 or 1
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


def get_mentorship_type(mentorship_type_str):
    """
    Returns ad-hoc, long-term, both or empty str
    """
    mentorship_type = mentorship_type_str.lower()

    if TYPE_AD_HOC in mentorship_type:
        return TYPE_AD_HOC.replace(' ', '-')
    elif TYPE_LONG_TERM in mentorship_type:
        return TYPE_LONG_TERM
    elif TYPE_BOTH in mentorship_type:
        return TYPE_BOTH
    return "NOT_FOUND"


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


def xlsx_to_yaml_parser(mentor_row, mentor_index):
    """
    Prepare mentor's excel data for yaml format
    """
    areas = get_yaml_block_sequence(mentor_row, AREAS_START_INDEX, AREAS_END_INDEX)
    focus = get_yaml_block_sequence(mentor_row, FOCUS_START_INDEX, FOCUS_END_INDEX)
    programming_languages = get_yaml_block_sequence(mentor_row, PROG_LANG_START_INDEX, PROG_LANG_END_INDEX)

    # TODO: If the complete yml is generated, these fields should be read from the old yml
    mentor_disabled = False
    mentor_matched = False
    mentor_sort = 10

    # Left commented since the code might be used in the later versions (if decided to
    # add default picture until the mentor's image is not available)
    # mentor_image = os.path.join(IMAGE_FILE_PATH, str(mentor_index) + IMAGE_SUFFIX)
    mentor_image = f"{IMAGE_FILE_PATH}/mentor_name_lowercase.jpeg # TODO take it from {mentor_row.iloc[12]}"

    mentor = {
        'name': mentor_row.iloc[1],
        'disabled': mentor_disabled,
        'matched': mentor_matched,
        'sort': mentor_sort,
        'hours': extract_numbers_from_string(mentor_row.iloc[29]),
        'type': get_mentorship_type(mentor_row.iloc[3]),
        'index': mentor_index,
        'location': mentor_row.iloc[5],
        'position': f"{mentor_row.iloc[7].strip()}, {mentor_row.iloc[8].strip()}",
        'bio': get_multiline_string(mentor_row.iloc[10]),
        'image': mentor_image,
        'languages': mentor_row.iloc[6],
        'availability': [],
        'skills': {
            'experience': mentor_row.iloc[9],
            'years': extract_numbers_from_string(mentor_row.iloc[9]),
            'mentee': get_multiline_string(mentor_row.iloc[28]),
            'areas': areas,
            'languages': ', '.join(programming_languages),
            'focus': focus,
            'extra': get_multiline_string(mentor_row.iloc[11]),
        },
        'network': get_social_media_links(mentor_row.iloc[30], mentor_row.iloc[31]),
    }
    return mentor


def get_all_mentors_in_yml_format(xlsx_file_path, skip_rows=0):
    """
    Read all mentors from Excel sheet.
    Prepare data for writing to yaml file.
    """
    # list of dict
    mentors = []

    df_mentors = pd.read_excel(xlsx_file_path, sheet_name=SHEET_NAME, skiprows=skip_rows)

    logging.info(f"Excel read {len(df_mentors)} mentors")

    for row in range(0, len(df_mentors)):
        mentor = xlsx_to_yaml_parser(df_mentors.iloc[row], row + 1)
        mentors.append(mentor)

    logging.info(f"Added {len(mentors)} mentors to the mentors.yml file")

    return mentors


def get_new_mentors_in_yml_format(yml_file_path, xlsx_file_path, skip_rows=1):
    """
    Read just new mentors from Excel sheet
     - start reading xlsx Mentors from the row 1 (from the date 03/04/2024)
     - find diff. between existing yml and xlsx
    Prepare data for writing to yaml file.
    """
    # list of dict
    mentors = []

    # Get mentors' names and indexes from yml file
    mentors_yml_dict = yml_utils.read_yml_to_dict(yml_file_path)

    df_mentors = pd.read_excel(xlsx_file_path, sheet_name=SHEET_NAME, skiprows=skip_rows)

    logging.info(f"Excel mentors: {len(df_mentors)}")

    if mentors_yml_dict:
        mentors_names_yml = [sub['name'].lower() for sub in mentors_yml_dict]
        mentors_indexes = [sub['index'] for sub in mentors_yml_dict]

        logging.info(f"Mentors yml total: {len(mentors_names_yml)}")

        # Highest index is used as the reference point from which
        # new indexes are calculated
        new_index = max(mentors_indexes) + 1

        # Get mentors' names from xlsx file
        mentors_names_xlsx = {}
        for i in range(0, len(df_mentors)):
            mentors_names_xlsx[i] = df_mentors.iloc[i].values[1].lower()

        for row, name in mentors_names_xlsx.items():
            if name not in mentors_names_yml:
                mentor = xlsx_to_yaml_parser(df_mentors.iloc[row], new_index)
                new_index += 1
                mentors.append(mentor)

        logging.info(f"Added {len(mentors)} mentors to the mentors.yml file")
    else:
        mentors = get_all_mentors_in_yml_format(xlsx_file_path, skip_rows)
    return mentors


def run_automation():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    if len(sys.argv) == 5:
        xlsx_file_path = sys.argv[1]
        yml_file_path = sys.argv[2]
        mode = WriteMode(sys.argv[3])
        skip_rows = int(sys.argv[4])

        logging.info("Params: xlsx: %s yml: %s mode: %s skip_rows: %s", xlsx_file_path, yml_file_path, mode, skip_rows)
    else:
        xlsx_file_path = "samples/mentors.xlsx"
        yml_file_path = "samples/mentors.yml"
        mode = WriteMode.APPEND
        skip_rows = 0

        logging.info("Default values: xlsx: %s yml:: %s mode: %s", xlsx_file_path, yml_file_path, mode)

    if mode == WriteMode.APPEND:
        logging.info("Appending option selected.")

        list_of_mentors = get_new_mentors_in_yml_format(yml_file_path, xlsx_file_path, skip_rows=skip_rows)

        logging.info("New Mentors size: %d", len(list_of_mentors))

        if list_of_mentors:
            write_yml_file(yml_file_path, list_of_mentors, WriteMode.APPEND)

    elif mode == WriteMode.WRITE.value:
        logging.info("Recreate yml - Write option selected.")

        list_of_mentors = get_all_mentors_in_yml_format(xlsx_file_path)
        write_yml_file(yml_file_path, list_of_mentors, WriteMode.WRITE)


if __name__ == "__main__":
    run_automation()
