import unittest
from naming_convention.utils.check_nc import check_nc, check_nc_folder, check_nc_file
from naming_convention.utils.args import SNAKE_CASE_REGEX, KEBAB_CASE_REGEX


class CheckNC(unittest.TestCase):
    def test_check_nc_snake_case(self):
        self.assertTrue(check_nc("snake_case", SNAKE_CASE_REGEX))
        self.assertFalse(check_nc("camelCase", SNAKE_CASE_REGEX))
        self.assertFalse(check_nc("kebab-case", SNAKE_CASE_REGEX))

    def test_check_nc_kebab_case(self):
        self.assertTrue(check_nc("kebab-case", KEBAB_CASE_REGEX))
        self.assertFalse(check_nc("camelCase", KEBAB_CASE_REGEX))
        self.assertFalse(check_nc("snake_case", KEBAB_CASE_REGEX))

    def test_check_nc_folder(self):
        folderpath = "/Users/user/folder_snake_case"
        self.assertFalse(check_nc_folder(folderpath, KEBAB_CASE_REGEX))

        folderpath = "Users/user/folder-kebab-case"
        self.assertTrue(check_nc_folder(folderpath, KEBAB_CASE_REGEX))

    def test_check_nc_file(self):
        filepath = "/Users/user/file-kebab-case.extension"
        self.assertFalse(check_nc_file(filepath, SNAKE_CASE_REGEX))

        filepath = "/Users/user/file_snake_case.extension"
        self.assertTrue(check_nc_file(filepath, SNAKE_CASE_REGEX))
