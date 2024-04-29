import os
import re
from naming_convention.utils.utils import get_filename, is_authorized_filename


def check_nc(name: str, nc_regex: re.Pattern) -> bool:
    return nc_regex.match(name)

def check_nc_folder(folderpath: str, nc_regex: str) -> bool:
    foldername = get_filename(folderpath)
    return check_nc(foldername, nc_regex)

def check_nc_file(filepath: str, nc_regex: str) -> bool:
    filename_with_ext = get_filename(filepath)
    if is_authorized_filename(filename_with_ext):
        return True
    filename_without_ext = os.path.splitext(filename_with_ext)[0]
    return check_nc(filename_without_ext, nc_regex)