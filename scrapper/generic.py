from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup


class GenericScrapper:
    def __init__(self):
        self.url = "https://statusinvest.com.br/"
        options = Options()
        self.driver = webdriver.Chrome(options=options)

    def call_url(self, url):
        self.driver.get(url)
        self.driver.implicitly_wait(2)
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
