from argparse import ArgumentParser
from os import system
from pathlib import Path
from shutil import rmtree
from sys import argv
from typing import Final

PAUSE_SHORT: Final[str] = "-p"
PAUSE_LONG: Final[str] = "--pause"


def parse_args() -> str:
    """
    Parses and returns arguments given to the program.
        Note that pause is not returned since we need to check for this flag even if parsing fails.
    """
    argument_parser: ArgumentParser = ArgumentParser()
    argument_parser.add_argument("stem", help="stem of .py file to freeze")
    argument_parser.add_argument(PAUSE_SHORT, PAUSE_LONG, action="store_true", help="pause after executing")
    stem: str = argument_parser.parse_args().stem
    return stem


def rmtree_if_dir(my_dir: str) -> None:
    """
    Deletes the tree at the given path if it exists.
    """
    path: Path = Path(my_dir)
    rmtree(path) if path.is_dir() else None


def unlink_if_file(file: str) -> None:
    """
    Deletes the file at the given path if it exists.
    """
    path: Path = Path(file)
    path.unlink() if path.is_file() else None


def clean(name: Path) -> None:
    """
    Deletes all files created by pyinstaller if they exist, except for the .exe file.
    """
    rmtree_if_dir("build")
    rmtree_if_dir("dist")
    rmtree_if_dir("__pycache__")
    unlink_if_file(f"{name.stem}.py.spec")


def to_exe(my_in: Path | str, out: Path | str) -> None:
    """
    Creates an .exe of the given .py file.
    :param my_in:
    :param out:
    :return:
    """
    """
    Creates an .exe of the given .py file.
    :param:
    Deletes build, dist, and pycache folders before and after compilation.
    """
    if isinstance(path, str):
        path = Path(path)
    clean(path)
    system(f"pyinstaller --onefile {path}")
    path: Path = Path(f"dist/{path}.exe")
    path.replace(f"{path}.exe") if path.is_file() else None
    clean(path)


def main() -> None:
    """
    Calls to_exe for the given stem (given as argument).
    """
    try:
        path: Path = Path(parse_args() + ".py")
        if path.is_file():
            to_exe(path)
        else:
            print(f"fatal: file {path} not found")
    except SystemExit:  # don't let the arg parser exit in case we need to pause
        pass
    if PAUSE_SHORT in argv or PAUSE_LONG in argv:
        input("paused -- press enter to exit\n")


if __name__ == "__main__":
    main()
