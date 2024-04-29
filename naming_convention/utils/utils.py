import re
import os
import json

AUTHORIZED_FILENAMES: set = set(["__main__.py", "__init__.py"])

CACHE_FILENAME = ".nc_cache.json"

SIZE_LIMIT = 1000


def verbose_diff(old_score: float, new_score: float):
    diff = round(new_score - old_score, 2)
    if diff >= 0:
        return f"+{diff}"
    else:
        return f"{diff}"


def cache_file_exists(base_path: str) -> bool:
    cache_file_path = os.path.join(base_path, CACHE_FILENAME)
    exists = os.path.exists(cache_file_path)
    if exists:
        content = get_cached_content(base_path)
        if content.get("base_path") == base_path:
            return True
    return False


def get_cached_content(base_path: str) -> dict:
    cache_file_path = os.path.join(base_path, CACHE_FILENAME)
    with open(cache_file_path, "r") as file:
        content : dict = json.load(file)
    return content


def create_cache_file(base_path: str, score: float) -> None:
    cache_file_path = os.path.join(base_path, CACHE_FILENAME)
    content = {"base_path": base_path, "score": score}
    with open(cache_file_path, "w") as file:
        json.dump(content, file)

def is_authorized_filename(filename: str):
    return filename in AUTHORIZED_FILENAMES

def is_valid_regex(regex: str):
    try:
        re.compile(regex)
        return True
    except re.error:
        return False

def get_filename(filepath: str) -> str:
    return os.path.basename(filepath)

def is_python_module(filepath: str) -> bool:
    return os.path.basename(filepath).endswith(".py")

def percentage_color(percentage: float):
    if percentage > 0.8:
        return "green"
    elif percentage > 0.5:
        return "yellow"
    else:
        return "red"
