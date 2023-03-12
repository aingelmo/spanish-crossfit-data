"""Module containing files needed for the selenium scraper."""
import logging
from datetime import datetime
from time import sleep

import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from src import config

DRIVER = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))


def run() -> None:
    """Run the URL extractor module."""
    logging.log(logging.INFO, "---Starting new process---")

    logging.log(logging.INFO, "Getting URLs to scrape...")
    spanish_metro_areas = get_spanish_metro_list()[-11:]
    crossfit_search_terms = get_crossfit_search_terms(spanish_metro_areas)
    urls_to_scrape = url_builder(spanish_metro_areas, crossfit_search_terms)

    for metro_area, search_term in urls_to_scrape.items():
        logging.log(logging.INFO, f"Scrapping {search_term}")

        DRIVER.get(search_term)
        sleep(2)

        while True:
            accept_cookies()
            sleep(5)

            logging.log(logging.INFO, f"Current URL - {DRIVER.current_url}")
            with open(f"{config.GOOGLE_HTML_DIR}/{metro_area}_{datetime.now()}.html", "w") as file:
                file.write(DRIVER.page_source)

            try:
                DRIVER.find_element(By.PARTIAL_LINK_TEXT, "Siguiente").click()
            except NoSuchElementException:
                logging.log(logging.WARNING, f"Nothing else found on: {search_term}")
                break


def get_spanish_metro_list() -> list[str]:
    """Get a list of all spanish metro areas from wikipedia"""
    r = requests.get("https://es.wikipedia.org/wiki/Anexo:%C3%81reas_metropolitanas_de_Espa%C3%B1a")
    soup = BeautifulSoup(r.text, "html.parser")
    spanish_pop_table = soup.find("table", {"class": "wikitable"})

    spanish_pop = pd.read_html(str(spanish_pop_table))
    spanish_pop = pd.DataFrame(spanish_pop[0])

    return spanish_pop["Área metropolitana"].sort_values().to_list()


def get_crossfit_search_terms(spanish_metro_areas: list[str]) -> list[str]:
    """Gets a list of all the terms to look in google based on the spanish metro areas"""
    return [f"Crossfit {metro_area.replace('-', ' ')} España" for metro_area in spanish_metro_areas]


def url_builder(spanish_metro_areas: list[str], search_terms: list[str]) -> dict[str, str]:
    """Creates a list of URLs to retrieve the results from."""
    return {
        spanish_metro_area.replace(
            "-", " "
        ): f"https://www.google.com/search?lr=lang_es&cr=countryES&hl=es&tbm=lcl&q={search_term}"
        for spanish_metro_area, search_term in zip(spanish_metro_areas, search_terms)
    }


def accept_cookies() -> None:
    """Accepts the cookies message if it pops up."""
    if "consent.google.com" in DRIVER.current_url:
        DRIVER.find_element(By.CSS_SELECTOR, "button[aria-label='Aceptar todo']").click()
