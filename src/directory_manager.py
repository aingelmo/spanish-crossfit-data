"""Manages all directory operations like creating or deleting dirs."""
from src import config


def create_directories() -> None:
    """Creates the directories to ensure the correct functioning of the script."""
    config.BOX_HTML_DIR.mkdir(exist_ok=True, parents=True)
    config.RAW_CSV_DIR.mkdir(exist_ok=True, parents=True)
