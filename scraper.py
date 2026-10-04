import sys
import json
# linting files
import os
from pathlib import Path

from datetime import datetime
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import requests
from dotenv import load_dotenv


load_dotenv()
api_key = os.environ.get("DISCORD_WEBHOOK_URL")

def send_discord_alert(message):
    """Sends a direct text alert to my Disc Channel."""
    payload = {"content": message}
    try:
        response = requests.post(api_key, json=payload)
        if response.status_code == 204:
            print("Alert successfully sent to your phone via Discord!")
        else:
            print(f"Failed to send alert. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error sending alert: {e}")


def fetch_page_title(url):
    print(f"Launching browser to look at: {url}...")

    
    with sync_playwright() as p:
        # Launch a background "headless" browser
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            # navigate to website and wait til network goes quiet:
            page.goto(url, wait_until="networkidle")

            # extra the raw html content:
            html_content = page.content()

            # parse the html with beautiful soup
            soup = BeautifulSoup(html_content, "html.parser")

            # find the main page heading (<h1>)
            main_heading = soup.find("h1")

            if main_heading:
                text_found = main_heading.get_text(strip=True)

                print(f"Success! Found Title: {text_found}")

                alert_text = f"Command Center Alert: Found <h1> on page: '{text_found}'"
                # send_discord_alert(alert_text)
                return text_found
            else:
                print("Connected to the page, but coudn't find an <h1> tag.")

        except Exception as e:
            print(f"An error occurred while grabbing the data: {e}")
        
        finally:
            browser.close()
        
if __name__ == "__main__":

    # test it with a basicc public site first to verify i works
    test_url = "https://www.gamewinners.com/index.html"

    today_date = datetime.now().strftime("%Y-%m-%d")

    log_path = Path("scraped_price_log.json")

    # if doesn't exist, or file is empty. create new data set...
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
                                "date" : today_date,
                                }
            log_path.write_text(json.dumps(log_data, indent=4))
            alert_text = f"Command Center Alert: New <h1> found: '{header_text}' \nDate: {today_date}"
            send_discord_alert(alert_text)
        else:
            print("No change detected. Standing by.")
            print(log_data)

    # if len(log_data) == 0:
    #     if header_text:
    #         log_data["item"] = {"header": header_text }
    #         print(log_data)        
    #         log_path.write_text(json.dumps(log_data, indent=4))
    # fetch_page_title(test_url)
    


