import json
import os

from datetime import datetime
from pathlib import Path

from scrapers.title_scrapers import fetch_page_title
from alerts.discord import send_discord_alert



if __name__ == "__main__":
    test_url = "https://gamewinners.com"

    today_date = datetime.now().strftime("%Y-%m-%d")

    log_path = Path("scraped_price_log.json")
    