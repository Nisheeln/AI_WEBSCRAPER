from selenium.webdriver.remote.webdriver import WebDriver as Remote
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

SBR_WEBDRIVER = "https://brd-customer-hl_a6dff71a-zone-ai_scrapper:pflun76z01mc@brd.superproxy.io:9515"

def scrape_website(website):
    print("Connecting to Scraping Browser...")
    sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, "goog", "chrome")
    chrome_options = ChromeOptions()

    with Remote(sbr_connection, options=chrome_options) as driver:
        driver.get(website)
        print("Waiting captcha to solve...")
        solve_res = driver.execute(
            "executeCdpCommand",
            {
                "cmd": "Captcha.waitForSolve",
                "params": {"detectTimeout": 10000},
            },
        )
        print("Captcha solve status:", solve_res["value"]["status"])
        print("Navigated! Scraping page content...")
        html = driver.page_source
        return html

# Reuse the same BeautifulSoup functions from above:
def extract_body_content(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body
    return str(body_content) if body_content else ""

def clean_body_content(body_content):
    soup = BeautifulSoup(body_content, "html.parser")
    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()
    return "\n".join(line.strip() for line in soup.get_text(separator="\n").splitlines() if line.strip())

def split_dom_content(dom_content, max_length=6000):
    return [dom_content[i : i + max_length] for i in range(0, len(dom_content), max_length)]
