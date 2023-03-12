"""Entrypoint of the app."""
from src import directory_manager, url_extractor, web_scraper

if __file__ == "__main__":
    directory_manager.create_directories()
    web_scraper.run()
    url_extractor.run()
