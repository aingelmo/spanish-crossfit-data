from pathlib import Path

import pandas as pd
from parsel import Selector

DATE = "20230903"
DATA = Path("data")
WORKING_DIR = DATA / DATE


if __name__ == "__main__":
    urls_list = []
    for html in WORKING_DIR.glob("*.html"):
        with open(html, "r") as file:
            content = file.read()

        selector = Selector(text=content)
        urls_in_html = selector.css("a[class='yYlJEf Q7PwXb L48Cpd brKmxb']").xpath("@href").getall()

        metro_area = html.stem.split("_")[0]

        for url in urls_in_html:
            urls_list.append((metro_area, url))

    urls_data = pd.DataFrame(urls_list, columns=["metro_area", "url"])
    urls_data.to_csv(DATA / "consolidated_urls.csv", index=False)
