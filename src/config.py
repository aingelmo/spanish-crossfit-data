"""Config module."""
import logging
from pathlib import Path

logging.basicConfig(
    filename="execution_logs.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
)

DATE = "20231203"

ROOT_DIR = Path(__file__).parents[1]
DATA_DIR = ROOT_DIR / "data"
DATE_DIR = ROOT_DIR / "data" / DATE
HTML_DIR = DATE_DIR / "html"
GOOGLE_HTML_DIR = HTML_DIR / "google"
BOX_HTML_DIR = HTML_DIR / "boxes"
RAW_CSV_DIR = DATE_DIR / "csv"

BOX_INFO = "div[class='VkpGBb']"
BOX_NAME = "span[class='OSrXXb']::text"
BOX_URL = "a[class='yYlJEf Q7PwXb L48Cpd brKmxb']"
