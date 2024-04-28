import argparse
import os
import json

KEBAB_CASE_REGEX = r"^[a-z]+(-[a-z]+)*$"
SNAKE_CASE_REGEX = r"^[a-z]+(_[a-z]+)*$"


def parse_args():
    parser = argparse.ArgumentParser(prog="NCPy")
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("-p", "--path", type=str, default=".")
    parser.add_argument("--fonc", "--folder-nc", type=str, default=KEBAB_CASE_REGEX)
    parser.add_argument("--finc", "--file-nc", type=str, default=SNAKE_CASE_REGEX)
    parser.add_argument("--force", action="store_true")
    parser.add_argument(
        "--varsnc", "--variables-nc", type=str, default=SNAKE_CASE_REGEX
    )
    parser.add_argument("--fail-under", type=float, default=0.7)
    parser.add_argument("-c", "--config-file", type=str)

    args: argparse.Namespace = parser.parse_args()
    config_file: str = args.config_file

    if config_file:
        if not os.path.exists(config_file):
            raise FileNotFoundError(f"{config_file} file does not exist")
        with open(config_file, "r") as file:
            args_from_file: dict = json.load(file)
        return argparse.Namespace(
            **args_from_file
        )  # to load key/value pairs from dict into namespace
    else:
        setattr(args, "authf", [])
        return args
