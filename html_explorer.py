import json
from pathlib import Path

import pandas as pd
from parsel import Selector

DATE = "20230903"
DATA = Path("data")
WORKING_DIR = DATA / DATE

urls_dict = {}
urls_list = []


for html in WORKING_DIR.glob("*.html"):
    with open(html, "r") as file:
        content = file.read()

    selector = Selector(text=content)
    urls_in_html = selector.css("a[class='yYlJEf Q7PwXb L48Cpd brKmxb']").xpath("@href").getall()

    metro_area = html.stem.split("_")[0]

    for url in urls_in_html:
        urls_list.append((metro_area, url))

    try:
        if urls_dict[metro_area]:
            for url in urls_in_html:
                urls_dict[metro_area].append(url)
    except KeyError:
        urls_dict[metro_area] = urls_in_html


with open("urls.json", "w") as file:
    json.dump(urls_dict, file, indent=4)


urls_data = pd.DataFrame(urls_list, columns=["metro_area", "url"])
urls_data.to_csv(DATA / "consolidated_urls.csv", index=False)
