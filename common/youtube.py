import os
import platform

import requests
from bs4 import BeautifulSoup
from commonlogging import CommonLogging
from dotenv import load_dotenv
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class YouTubeScraper:
    def __init__(self, url):
        platformName = platform.system()
        platformArchitecher = platform.machine()
        os.environ["WDM_LOG"] = "0"

        if platformArchitecher == "aarch64":
            os.environ["WDM_ARCH"] = "arm64"
        elif platformArchitecher == "arm64":
            os.environ["WDM_ARCH"] = "arm64"
        else:
            os.environ["WDM_ARCH"] = "x64"

        self.url = url

    def scrape(self):
        selenium_use = True
        html = None

        if selenium_use:
            options = webdriver.ChromeOptions()
            options.add_experimental_option("excludeSwitches", ["enable-logging"])
            options.add_experimental_option("detach", True)
            options.add_argument("headless")
            options.add_argument("no-sandbox")
            options.add_argument("disable-dev-shm-usage")
            options.add_argument("window-size=1920x1080")
            options.add_argument("disable-gpu")
            # https://kangmanjoo.tistory.com/122
            options.add_argument("--log-level=3")
            options.add_argument("--disable-loging")
            options.add_argument(UserAgent().chrome)

            serviceDriver = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=serviceDriver, options=options)

            driver.get(self.url)
            html = driver.page_source
        else:
            response = requests.get(self.url)
            if response.status_code == 200:
                html = response.text
            else:
                print("Failed to load the page. Status code:", response.status_code)

        soup = BeautifulSoup(html, "html.parser")
        # soup = BeautifulSoup(html)
        # soup = BeautifulSoup(html, 'lxml')
        # soup = BeautifulSoup(html, 'html5lib')
        # soup = BeautifulSoup(html)
        cards = soup.find_all("ytd-vertical-product-card-renderer")

        text = ""
        cnt = 0
        for index, card in enumerate(cards):
            # aria_label = card.find('a')['aria-label']
            # print(aria_label)
            product_name_element = card.find("div", {"id": "product-name"})
            price_element = card.find("span", {"id": "price"})
            if product_name_element:
                # print(product_name_div.text)
                if index == len(cards) - 1:  # 마지막 카드인 경우
                    text += product_name_element.text + "[" + price_element.text.replace(",", "").replace("₩", "") + "]"
                    cnt += 1
                else:
                    text += product_name_element.text + "[" + price_element.text.replace(",", "").replace("₩", "") + "]" + ","
                    cnt += 1
        print(cnt, text)
        logger.info(str(cnt) + " " + text)
        if selenium_use:
            driver.quit()
            # driver.close()


if __name__ == "__main__":
    load_dotenv()
    youtube_url = os.getenv("YOUTUBE_CRAWLING_URL")
    logFileName = os.path.expanduser("~") + "/youtube.log"
    logger = CommonLogging(logFileName).logger
    scraper = YouTubeScraper(youtube_url)
    scraper.scrape()
