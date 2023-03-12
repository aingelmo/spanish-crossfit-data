"""Entrypoint of the app."""
from src import directory_manager, google_url_web_scraper, url_extractor

if __name__ == "__main__":
    directory_manager.create_directories()
    # google_url_web_scraper.run()
    url_extractor.run()
