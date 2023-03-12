"""Download the urls from the consolidated csv."""
import logging
from pathlib import Path

import pandas as pd
import requests

from src import config


def run() -> None:
    """Run the methods in the module."""
    consolidated_urls = read_csv(config.DATE_DIR / "urls_consolidated.csv")
    consolidated_urls = remove_null_values(consolidated_urls)

    all_metro_areas = consolidated_urls["metro_area"].unique()

    for metro_area in all_metro_areas:
        create_metro_area_directories(metro_area)
        for row in consolidated_urls.query("metro_area == @metro_area").iterrows():
            print(row)
            url_response = get_url_response(row[1]["box_url"])
            save_html_from_response(url_response, metro_area, row[1]["box_name"])


def read_csv(consolidated_csv_path: str | Path) -> pd.DataFrame:
    """Reads the consolidated csv."""
    return pd.read_csv(consolidated_csv_path)


def remove_null_values(consolidated_csv: pd.DataFrame) -> pd.DataFrame:
    """Removes the null values from the consolidated urls dataset."""
    return consolidated_csv.dropna(subset="box_url")


def create_metro_area_directories(metro_area: str) -> None:
    """Create the metro area directory to ensure correct functioning."""
    metro_area_box_dir = config.BOX_HTML_DIR / metro_area
    metro_area_box_dir.mkdir(exist_ok=True, parents=True)


def get_url_response(url: str) -> requests.Response | None:
    """Gets the URL response."""
    try:
        return requests.get(url)
    except requests.exceptions.ConnectionError:
        logging.log(logging.ERROR, f"Couldn't connect to {url}")
        return None


def save_html_from_response(url_response: requests.Response | None, metro_area: str, box_name: str) -> None:
    """Extract the html from the website and store it in the correct form."""
    if url_response is None:
        return None

    if url_response.status_code == 400:
        logging.log(logging.ERROR, f"Unable to fetch {url_response.url}")
        return None

    with open(config.BOX_HTML_DIR / metro_area / f"{box_name}.html", "w") as html_file:
        html_file.write(url_response.text)
