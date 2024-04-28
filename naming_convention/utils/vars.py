import ast


def find_modules_vars(filepath: str) -> set:
    try:
        with open(filepath, "r") as file:
            tree = ast.parse(file.read())

        file_vars = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        file_vars.add(target.id)
            if isinstance(node, ast.FunctionDef):
                for argument in node.args.args:
                    file_vars.add(argument.arg)
            if isinstance(node, ast.AnnAssign):
                try:
                    file_vars.add(node.target.id)
                except AttributeError:
                    pass

        return file_vars
    except:
        return set()


if __name__ == "__main__":
    print(find_modules_vars("naming_convention/utils/utils.py"))
