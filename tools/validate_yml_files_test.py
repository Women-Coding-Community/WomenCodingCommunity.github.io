import unittest

import yml_utils as utils
from file_utils import TOOLS_PATH, DATA_PATH


class ValidateYmlFilesTest(unittest.TestCase):

    def test_open_yml_success_sample(self):
        result = utils.read_yml_to_dict(TOOLS_PATH + "/samples/mentors.yml")

        self.assertGreater(len(result), 0, "the sample yml is valid")
        self.assertEqual("Mentor1", result[0]['name'])

    def test_invalid_yml_file(self):
        result = utils.read_yml_to_dict(TOOLS_PATH + "/features/invalid.yml")

        self.assertEqual({}, result)

    def test_all_data_files(self):
        file_names = ["mentors.yml", "announcement.yml", "books.yml", "collaborators.yml", "faq.yml", "footer.yml",
                      "index.yml", "navbar.yml", "programmes.yml", "resources.yml", "team.yml", "reviews.yml"]

        for file_name in file_names:
            result = utils.read_yml_to_dict(DATA_PATH + "/" + file_name)
            self.assertGreater(len(result), 0, f"_data/{file_name} is invalid.")
