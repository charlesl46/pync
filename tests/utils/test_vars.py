import unittest
from naming_convention.utils.vars import find_modules_vars
from naming_convention.utils.args import SNAKE_CASE_REGEX, KEBAB_CASE_REGEX


class TestVars(unittest.TestCase):
    def test_vars_from_module(self):
        vars = find_modules_vars("tests/utils/assets/module.py")
        self.assertEqual(vars,set(['param_ok', 'paramNotOk', 'variableNotOk', 'variable_ok']))

        vars = find_modules_vars("tests/utils/assets/empty_module.py")
        self.assertEqual(vars,set())