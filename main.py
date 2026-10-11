import json
import os

from datetime import datetime
from pathlib import Path

from scrapers.title_scraper import fetch_page_title
from alerts.discord import send_discord_alert



if __name__ == "__main__":
    test_url = "https://gamewinners.com"

    today_date = datetime.now().strftime("%Y-%m-%d")

    log_path = Path("scraped_price_log.json")
    
    # if it doesn't exist or file empty; create a new data set
    if not log_path.exists() or log_path.stat().st_size == 0:
        log_data = {}
    else:
        log_data = json.loads(log_path.read_text())
    
    header_text = fetch_page_title(test_url)

    if header_text:
        old_header = log_data.get("item", {}).get("header")
        old_date = log_data.get("item", {}).get("date")

        if header_text != old_header or today_date != old_date:
            print("Change detected! Updating log and sending alert...")
            log_data["item"] = {"header": header_text,
                                "date": today_date,
                                }
            log_path.write_text(json.dumps(log_data, indent=4))
            alert_text = f"Command Center Alert: New <h1> found: '{header_text}' \nDate: {today_date}"
            send_discord_alert(alert_text)
        else:
            print("No change detected. Standing by.")
            print(log_data)
