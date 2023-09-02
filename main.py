import json
from scrapper.types import STOCKS_BR
from scrapper.scrapper_constructor import ScrapperConstructor
from google_sheet_invest import GoogleSheetInvest


def get_invest_data():
    scraper_stock_br = ScrapperConstructor().build(STOCKS_BR)

    tickets = [
        {"ticket": "EGIE3"},
        {"ticket": "GGBR4"},
        {"ticket": "ITUB4"},
        {"ticket": "KLBN11"},
        {"ticket": "VALE3"},
        {"ticket": "VIVT3"},
    ]

    tickets_info = []

    for ticket in tickets:
        print(f"Getting data from {ticket['ticket']}")
        data = scraper_stock_br.get_data(ticket["ticket"])
        print(data)
        tickets_info.append(data)

    scraper_stock_br.driver_quit()

    with open("extractions/data.json", "w") as file:
        json.dump(tickets_info, file, indent=4)


# You need to create a service account on google cloud platform, download the json file and put it on the root folder as service_account_credential.json
# You need share the google sheet with the email on the json file
def save_invest_data_on_google_sheet():
    gs_invest = GoogleSheetInvest()
    gs_invest.save_data(STOCKS_BR)


def main():
    get_invest_data()
    save_invest_data_on_google_sheet()


if __name__ == "__main__":
    main()
