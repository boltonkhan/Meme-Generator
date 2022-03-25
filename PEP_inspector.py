"""Run pydocstyle and pycodestyle for all poject files."""

import pathlib
import subprocess
from typing import List

from click import command

from Helpers import Utilities as util


def collect_files(ignored_files: List[str]) -> List[pathlib.Path]:
    """Get all python files from the poject.

    :return: all python project files
    :rtype: List[str]
    """
    files = util.find_files_by_ext('.', '.py', "venv")
    for file in ignored_files:
        files = list(
            filter(lambda f: False if str(f).endswith(file) else True,
                   files
                   )
        )

    return files


def run_pydocstyle(command: str, files: List[str]) -> None:
    """Run pydocstyle on all files."""
    for file in files:
        proc = subprocess.Popen([command, f"{file}"])
        try:
            outs, errs = proc.communicate(timeout=15)
        except subprocess.TimeoutExpired:
            proc.kill()
            outs, errs = proc.communicate


if __name__ == "__main__":
    """Start execution."""
    commands = ["pydocstyle", "pycodestyle"]

    ignored = [  # ignore files with a given name
        "__init__.py",
        "aws_test.py",
        "test.py",
        "test_goodreads.py",
        "test_scrap.py",
        "test_unsplash.py"
    ]

    files = collect_files(ignored)

    for command in commands:
        print(command, '------------------')
        run_pydocstyle(command, files)
        print('----------------------------')
