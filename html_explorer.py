from datetime import datetime
from pathlib import Path

import pandas as pd
from parsel import Selector

DATE = "20230903"
DATA = Path("data")
RAW_DATA_DIR = DATA / DATE / "raw"
CSV_DATA_DIR = DATA / DATE / "csv"


BOX_INFO = "div[class='VkpGBb']"
BOX_NAME = "span[class='OSrXXb']::text"
BOX_URL = "a[class='yYlJEf Q7PwXb L48Cpd brKmxb']"


def get_content(html_file_path: Path) -> Selector:
    """Opens up an html file and return the parsel selector ready to use."""
    with open(html_file_path) as file:
        html_content = file.read()
        return Selector(text=html_content)


def get_box_info_content(selector: Selector) -> list[str]:
    """Returns all the information boxes present in the selector object."""
    return selector.css(BOX_INFO).getall()


def get_box_name_url(box_info_content: str) -> tuple[str, str]:
    """Returns the box name and correspondent url from the information box."""
    box_content = Selector(text=box_info_content)
    box_name = box_content.css(BOX_NAME).get()
    box_url = box_content.css(BOX_URL).xpath("@href").get()
    return (box_name, box_url)


def create_metro_box_data(box_info_list: list[tuple[str, str]], filename: str) -> None:
    """Save a csv file with all the boxes names and urls from the correspondent metro area."""
    metro_box_df = pd.DataFrame(box_info_list, columns=["box_name", "box_url"])
    metro_box_df.to_csv(DATA / DATE / "csv" / f"{filename}_{datetime.now()}.csv", index=False)


def create_consolidated_data(csv_path: Path) -> None:
    """Scan the folder to find csv files and returns a consolidated dataframe with all together."""
    df_to_concat = []
    for csv in csv_path.glob("*.csv"):
        metro_area = csv.stem.split("_")[0]
        temp_csv_data = pd.read_csv(csv)
        temp_csv_data = temp_csv_data.assign(metro_area=metro_area)
        df_to_concat.append(temp_csv_data)
    all_csvs_data = pd.concat(df_to_concat)[["metro_area", "box_name", "box_url"]]
    all_csvs_data.to_csv(DATA / DATE / "urls_consolidated.csv", index=False)


if __name__ == "__main__":
    for html_file in list(RAW_DATA_DIR.glob("*.html")):
        metro_area = html_file.stem.split("_")[0]

        main_file_selector = get_content(html_file)

        boxes_with_content = get_box_info_content(main_file_selector)

        box_info_list = [get_box_name_url(box_information) for box_information in boxes_with_content]

        create_metro_box_data(box_info_list, metro_area)

    create_consolidated_data(CSV_DATA_DIR)
