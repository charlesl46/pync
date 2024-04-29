import unittest
import random
import os

from naming_convention.utils.utils import verbose_diff,cache_file_exists,get_cached_content,create_cache_file,CACHE_FILENAME

class TestUtils(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.folder_with_cache_file_path = "tests/utils/assets/folder_with_cache_file"
        self.folder_without_cache_file_path = "tests/utils/assets/folder_without_cache_file"

    def test_verbose_diff(self):
        NB_TESTS = 1000
        for _ in range(NB_TESTS):
            old_score = round(random.random(),1)
            new_score = round(random.random(),1)
            diff = verbose_diff(old_score,new_score)
            real_diff = round(new_score - old_score,1)
            if new_score >= old_score:
                self.assertEqual(diff,f"+{real_diff}")
            else:
                self.assertEqual(diff,f"{real_diff}")

    def test_cache_file_exists(self):
        self.assertTrue(cache_file_exists(self.folder_with_cache_file_path))
        self.assertFalse(cache_file_exists(self.folder_without_cache_file_path))

    def test_get_cached_content(self):
        content = {"base_path" : self.folder_with_cache_file_path,"score" : 0.5}
        self.assertEqual(get_cached_content(self.folder_with_cache_file_path),content)

    def test_create_cache_file(self):
        create_cache_file(self.folder_without_cache_file_path,score=0.5)
        self.assertTrue(cache_file_exists(self.folder_without_cache_file_path))
        os.remove(os.path.join(self.folder_without_cache_file_path,CACHE_FILENAME))
        self.assertFalse(cache_file_exists(self.folder_without_cache_file_path))