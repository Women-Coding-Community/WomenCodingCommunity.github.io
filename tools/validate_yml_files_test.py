import os
import unittest

import yml_utils as utils


class ValidateYmlFilesTest(unittest.TestCase):

    def test_open_yml_success_sample(self):
        result = utils.read_yml_to_dict("samples/mentors.yml")

        self.assertEqual(len(result), 1)
        self.assertEqual("Mentor1", result[0]['name'])

    def test_invalid_yml_file(self):
        result = utils.read_yml_to_dict("features/invalid.yml")

        self.assertEqual({}, result)

    def test_all_data_files(self):
        data_folder = os.path.abspath(os.curdir).replace("tools", "_data/")

        file_names = ["mentors.yml", "announcement.yml", "books.yml", "collaborators.yml", "faq.yml", "footer.yml",
                      "index.yml", "navbar.yml", "programmes.yml", "resources.yml", "team.yml", "reviews.yml"]

        for file_name in file_names:
            result = utils.read_yml_to_dict(data_folder + file_name)
            self.assertGreater(len(result), 0, f"_data/{file_name} is invalid.")
