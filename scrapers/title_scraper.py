
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

def fetch_page_title(url: str):

    print(f"Launching browser to fetch page at url: {url}...")

    with sync_playwright() as p:

        # Launch a background "headless" browser
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            # navigate to page and wait til network goes quiet
            page.goto(url, wait_until="networkidle")

            # extract raw html content:
            html_content = page.content()

            soup = BeautifulSoup(html_content, "html.parser")

            # Find the main page heading (<h1>)
            main_heading = soup.find("h1")

            if main_heading:
                text = main_heading.get_text(strip=True)
                print(f"Success! Found Title: {text}")
                
                return text
            else:
                print("Connected to the page, but couldn't find an <h1> tag.")

        except Exception as e:
            print(f"An error occurred while grabbing the data: {e}")
        
        finally:
            browser.close()

    


     