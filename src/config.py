"""Config module."""
import logging
from pathlib import Path

logging.basicConfig(
    filename="execution_logs.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
)

DATE = "20230903"

ROOT_DIR = Path(__file__).parents[1]
DATA_DIR = ROOT_DIR / "data"
DATE_DIR = ROOT_DIR / "data" / DATE
HTML_DIR = DATE_DIR / "html"
GOOGLE_HTML_DIR = HTML_DIR / "google"
BOX_HTML_DIR = HTML_DIR / "boxes"
RAW_CSV_DIR = DATA_DIR / "csv"
