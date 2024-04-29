import unittest
from naming_convention.utils.check_nc import check_nc, check_nc_folder, check_nc_file
from naming_convention.utils.args import SNAKE_CASE_REGEX, KEBAB_CASE_REGEX
import re

class TestCheckNC(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.snake_case_regex = re.compile(SNAKE_CASE_REGEX)
        self.kebab_case_regex = re.compile(KEBAB_CASE_REGEX)

    def test_check_nc_snake_case(self):
        self.assertTrue(check_nc("snake_case", self.snake_case_regex))
        self.assertFalse(check_nc("camelCase", self.snake_case_regex))
        self.assertFalse(check_nc("kebab-case", self.snake_case_regex))

    def test_check_nc_kebab_case(self):
        self.assertTrue(check_nc("kebab-case", self.kebab_case_regex))
        self.assertFalse(check_nc("camelCase", self.kebab_case_regex))
        self.assertFalse(check_nc("snake_case", self.kebab_case_regex))

    def test_check_nc_folder(self):
        folderpath = "/Users/user/folder_snake_case"
        self.assertFalse(check_nc_folder(folderpath, self.kebab_case_regex))

        folderpath = "Users/user/folder-kebab-case"
        self.assertTrue(check_nc_folder(folderpath, self.kebab_case_regex))

    def test_check_nc_file(self):
        filepath = "/Users/user/file-kebab-case.extension"
        self.assertFalse(check_nc_file(filepath, self.snake_case_regex))

        filepath = "/Users/user/file_snake_case.extension"
        self.assertTrue(check_nc_file(filepath, self.snake_case_regex))
