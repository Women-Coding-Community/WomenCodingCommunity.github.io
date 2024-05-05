import logging

from ruamel.yaml import YAML
from ruamel.yaml.scanner import ScannerError


def read_yml_to_dict(file_path):
    """
    Read yml file and convert to dictionary
    """
    try:
        with open(file_path, 'r', encoding="utf-8") as input_yml:
            yaml = YAML(typ='safe')
            yml_dict = yaml.load(input_yml)

            logging.info("File: %s is successfully read.", file_path)

            return yml_dict
    except ScannerError as ex:
        logging.error("Invalid yml file %s.", file_path)
        return {}
