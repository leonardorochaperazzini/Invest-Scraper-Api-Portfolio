import os
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from app.FakeUserAgent import FakeUserAgent

class GenericScrapper:
    def __init__(self):
        self.url = "https://statusinvest.com.br/"
        options = webdriver.FirefoxOptions()
        options.add_argument(f"user-agent={FakeUserAgent().get_random_user_agent()}")

        self.driver = webdriver.Remote(
            command_executor=os.getenv('SELENIUM_HUB_URL', 'http://selenium-hub:4444'),
            options=options
        )

    def call_url(self, url):
        self.driver.get(url)
        self.driver.implicitly_wait(2)
        time.sleep(1)
        return BeautifulSoup(self.driver.page_source, "html.parser")

    def convert_to_float(self, value):
        if value.strip() == "-":
            return "-"
        return float(value.replace(".", "").replace(",", ".").replace("%", ""))

    def get_data(self, ticker):
        try:
            return self.get_data_from_ticker(ticker)
        except Exception as e:
            return {
                "ticker": ticker,
                "type": self.type,
                "error": "Failed to get data",
                "error_cause": str(e),
            }

    def driver_quit(self):
        self.driver.quit()
