import os
import sys
import re

from rich.console import Console
from rich.progress import track

from naming_convention.utils.args import parse_args
from naming_convention.utils.check_nc import check_nc_file, check_nc_folder, check_nc
from naming_convention.utils.utils import (
    percentage_color,
    is_valid_regex,
    is_python_module,
    cache_file_exists,
    get_cached_content,
    create_cache_file,
    verbose_diff,
    SIZE_LIMIT,
)
from naming_convention.utils import utils
from naming_convention.utils.vars import find_modules_vars


class Parser:
    def __init__(
        self,
        path: str,
        folder_nc_regex: str,
        file_nc_regex: str,
        vars_nc_regex: str,
        authorized_filenames: list,
        verbose: bool,
        fail_under: float,
        force: bool,
    ) -> None:
        self.path = os.path.abspath(path)

        if is_valid_regex(folder_nc_regex):
            self.folder_nc_regex = re.compile(folder_nc_regex)
        else:
            raise Exception(f"The regex {folder_nc_regex} is not valid")

        if is_valid_regex(file_nc_regex):
            self.file_nc_regex = re.compile(file_nc_regex)
        else:
            raise Exception(f"The regex {file_nc_regex} is not valid")

        if is_valid_regex(vars_nc_regex):
            self.vars_nc_regex = re.compile(vars_nc_regex)
        else:
            raise Exception(f"The regex {vars_nc_regex} is not valid")

        utils.AUTHORIZED_FILENAMES = set(authorized_filenames)
        self.verbose = verbose
        self.folders_checked_ok = 0
        self.folders_checked_nok = 0
        self.files_checked_ok = 0
        self.files_checked_nok = 0
        self.vars_checked_ok = 0
        self.vars_checked_nok = 0
        self.console = Console()
        self.fail_under = fail_under
        self.force = force

    @property
    def print(self):
        return self.console.print

    def check_path(self) -> None:
        walked = list(os.walk(self.path))
        total = len(walked)
        if total > SIZE_LIMIT and not self.force:
            self.print(
                f"The folder {self.path} has a file structure of size = {total}, the parsing could be long. If you really want to parse this path, add option --force"
            )
            sys.exit(1)
        for path, dirnames, filenames in track(
            walked, f"Checking {self.path}", console=self.console, total=total
        ):
            for dirname in dirnames:
                real_path = os.path.join(self.path, path, dirname)
                # if os.path.isdir(real_path): # maybe useless
                is_ok = self.check_nc_folder(real_path)
                if self.verbose:
                    if is_ok:
                        self.print(f"FOLDER {real_path} ok", style="green")
                    else:
                        self.print(f"FOLDER {real_path} nok", style="red bold")

            for filename in filenames:
                real_path = os.path.join(self.path, path, filename)
                # if os.path.isfile(real_path): # maybe useless
                if is_python_module(real_path):
                    is_ok = self.check_nc_file(real_path)
                    if self.verbose:
                        if is_ok:
                            self.print(f"FILE {real_path} ok", style="green")
                        else:
                            self.print(f"FILE {real_path} nok", style="red bold")
                    self.check_vars_file(real_path)
        self.show_stats()

    def check_nc_file(self, filepath: str) -> bool:
        ok = check_nc_file(filepath, self.file_nc_regex)
        if ok:
            self.files_checked_ok += 1
        else:
            self.files_checked_nok += 1
        return ok

    def check_nc_var(self, variable_name: str):
        ok = check_nc(variable_name, self.vars_nc_regex)
        if ok:
            self.vars_checked_ok += 1
        else:
            self.vars_checked_nok += 1
        return ok

    def check_vars_file(self, filepath: str):
        variables = find_modules_vars(filepath)
        if len(variables) > 0:
            if self.verbose:
                self.print(f"MODULE VARS {filepath}")
            for variable in variables:
                is_ok = self.check_nc_var(variable)
                if self.verbose:
                    if not is_ok:
                        self.print(f"\tVARIABLE {variable} nok", style="red italic")
                    else:
                        self.print(f"\tVARIABLE {variable} ok", style="green italic")

    def check_nc_folder(self, folderpath: str) -> bool:
        ok = check_nc_folder(folderpath, self.folder_nc_regex)
        if ok:
            self.folders_checked_ok += 1
        else:
            self.folders_checked_nok += 1
        return ok

    @property
    def total_folders_checked(self) -> int:
        return self.folders_checked_nok + self.folders_checked_ok

    @property
    def total_files_checked(self) -> int:
        return self.files_checked_nok + self.files_checked_ok

    @property
    def total_vars_checked(self) -> int:
        return self.vars_checked_nok + self.vars_checked_ok

    def show_stats(self) -> None:
        self.print(f"Parsing of {self.path} completed", style="bold", justify="center")

        if self.total_folders_checked > 0:
            percentage_folders_ok = self.folders_checked_ok / self.total_folders_checked
            self.print(
                f"{round(percentage_folders_ok * 100,0)} % folders ok",
                style=percentage_color(percentage_folders_ok),
            )
            self.print(f"{self.total_folders_checked} folders checked")

            self.print("\n")
        else:
            percentage_folders_ok = 1

        if self.total_files_checked > 0:
            percentage_files_ok = self.files_checked_ok / self.total_files_checked
            self.print(
                f"{round(percentage_files_ok * 100,0)} % files ok",
                style=percentage_color(percentage_files_ok),
            )
            self.print(f"{self.total_files_checked} files checked")

            self.print("\n")
        else:
            percentage_files_ok = 1

        if self.total_vars_checked > 0:
            percentage_vars_ok = self.vars_checked_ok / self.total_vars_checked
            self.print(
                f"{round(percentage_vars_ok * 100,0)} % vars ok",
                style=percentage_color(percentage_vars_ok),
            )
            self.print(f"{self.total_vars_checked} vars checked")
        else:
            percentage_vars_ok = 1

        mean = round(
            (percentage_files_ok + percentage_folders_ok + percentage_vars_ok) / 3, 2
        )

        if cache_file_exists(self.path):
            cached_mean = get_cached_content(self.path).get("score")
        else:
            cached_mean = None

        create_cache_file(self.path, mean)

        if mean < self.fail_under:
            if cached_mean:
                sys.stderr.write(
                    f"Failed, {mean} mean mark is below threshold : {self.fail_under} (precedent : {cached_mean} ({verbose_diff(cached_mean,mean)}))"
                )
            else:
                sys.stderr.write(
                    f"Failed, {mean} mean mark is below threshold : {self.fail_under}"
                )

            sys.exit(1)  # error for pipelines
        else:
            if cached_mean:
                sys.stdout.write(
                    f"Success, {mean} mean mark is above threshold : {self.fail_under} (precedent : {cached_mean} ({verbose_diff(cached_mean,mean)}))"
                )
            else:
                sys.stdout.write(
                    f"Success, {mean} mean mark is above threshold : {self.fail_under}"
                )

            sys.exit(0)


def main():
    args = parse_args()
    parser = Parser(
        path=args.path,
        folder_nc_regex=args.fonc,
        file_nc_regex=args.finc,
        vars_nc_regex=args.varsnc,
        authorized_filenames=args.authf,
        verbose=args.verbose,
        fail_under=args.fail_under,
        force=args.force,
    )
    parser.check_path()


if __name__ == "__main__":
    main()
