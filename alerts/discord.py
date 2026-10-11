import os
import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("DISCORD_WEBHOOK_URL")

def send_discord_alert(message: str) -> None:
    """Sends a direct text alert to my Disc Channel."""
    if not api_key:
        print(f"Error: Discword Webhook URL not found in environment variables.")
        return
    payload = { "content": message}
    try:
        res = requests.post(api_key, json=payload)
        if res.status_code == 204:
            print("Alert successfully sent to Discord!")
        else:
            print(f"Failed to send alert. Status code: {res.status_code}.")
    except Exception as e:
        print(f"Error sending alert: {e}")
