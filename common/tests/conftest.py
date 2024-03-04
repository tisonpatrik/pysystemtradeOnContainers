import sys
from pathlib import Path


def pytest_configure():
    # Base directory for the project
    root_dir = Path(__file__).parent.parent

    # Paths to add to sys.path, pointing to the base of `data_management` and `common`
    paths_to_add = [root_dir]

    # Convert paths to strings and add them to sys.path if not already included
    for path in paths_to_add:
        str_path = str(path)
        if str_path not in sys.path:
            sys.path.insert(0, str_path)

    # Print sys.path for debugging
    print("Modified sys.path to include:", *paths_to_add, sep="\n")
