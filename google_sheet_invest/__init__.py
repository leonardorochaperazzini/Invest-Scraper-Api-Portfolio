import pygsheets
import json
import pandas as pd
from scrapper.types import STOCKS_BR


class GoogleSheetInvest:
    def __init__(self):
        gc = pygsheets.authorize(service_file="service_account_credential.json")
        self.sh = gc.open("Investimento e fundo Leonardo")

    def __get_extractions(self):
        with open("extractions/data.json") as file:
            return json.load(file)

    def __change_numeric_to_be_saved(self, df):
        for column in df.columns:
            if df[column].dtype == "float64":
                df[column] = df[column].apply(lambda x: str(x).replace(".", ","))

    def save_data(self, type):
        data = self.__get_extractions()

        if type == STOCKS_BR:
            init_pos = (4, 6)
            wks = self.sh.worksheet_by_title("Ações BR")

        sheet_df = wks.get_as_df(has_header=True, index_colum=0, empty_value="")
        df_ticker = sheet_df["TICKER"]

        df = pd.DataFrame(data)
        df_ticker = df_ticker[df_ticker.isin(df["ticker"])]
        df = df.set_index("ticker").loc[df_ticker].reset_index()

        df = df.drop(columns=["ticker", "type"])
        self.__change_numeric_to_be_saved(df)
        wks.set_dataframe(df, init_pos, copy_head=False)
