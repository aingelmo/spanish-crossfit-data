"""Entrypoint of the app."""
from src import directory_manager, web_scraper

if __file__ == "__main__":
    directory_manager.create_directories()
    web_scraper.run()
