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


def to_exe(stem: str) -> None:
    """
    Creates an .exe of the .py file with the given stem.
    The given .py file must be in the same directory as this file.
    The .exe appears in the same directory as this file.
    Deletes build, dist, and pycache folders before and after compilation.
    """
    rmtree("build") if Path("build").is_dir() else None
    rmtree("dist") if Path("dist").is_dir() else None
    rmtree("__pycache__") if Path("__pycache__").is_dir() else None
    system(f"pyinstaller --onefile {stem}.py")
    Path(f"dist/{stem}.exe").replace(f"{stem}.exe")
    rmtree("build")
    Path("dist").rmdir()
    rmtree("__pycache__")
    Path(f"{stem}.spec").unlink()


def main() -> None:
    """
    Calls to_exe for the given stem (given as argument).
    """
    try:
        name: str = parse_args() + ".py"
        if Path(name).is_file():
            to_exe(name)
        else:
            print(f"fatal: file {name} not found")
    except SystemExit:  # don't let the arg parser exit in case we need to pause
        pass
    if PAUSE_SHORT in argv or PAUSE_LONG in argv:
        input("paused -- press enter to exit\n")


if __name__ == "__main__":
    main()
