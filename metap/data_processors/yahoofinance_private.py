"""Reference: https://github.com/AI4Finance-LLC/FinRL"""
from typing import List

import numpy as np
import pandas as pd
import pytz
import yfinance as yf

try:
    import exchange_calendars as tc
except:
    print(
        "Cannot import exchange_calendars.",
        "If you are using python>=3.7, please install it.",
    )
    import trading_calendars as tc

    print("Use trading_calendars instead for yahoofinance processor..")

from meta.config import (
    BINANCE_BASE_URL,
    TIME_ZONE_BERLIN,
    TIME_ZONE_JAKARTA,
    TIME_ZONE_PARIS,
    TIME_ZONE_SELFDEFINED,
    TIME_ZONE_SHANGHAI,
    TIME_ZONE_USEASTERN,
    USE_TIME_ZONE_SELFDEFINED,
)
from meta.data_processors._base import _Base, calc_time_zone
from meta.data_processors.yahoofinance import Yahoofinance


class YahoofinancePrivate(Yahoofinance):
    def __init__(
        self,
        data_source: str,
        start_date: str,
        end_date: str,
        time_interval: str,
        **kwargs
    ):
        super().__init__(data_source, start_date, end_date, time_interval, **kwargs)

    def download_data(self, ticker_list: List[str], proxy):
        self.time_zone = calc_time_zone(
            ticker_list, TIME_ZONE_SELFDEFINED, USE_TIME_ZONE_SELFDEFINED
        )
        self.dataframe = pd.DataFrame()
        for tic in ticker_list:
            temp_df = yf.download(
                tic,
                start=self.start_date,
                end=self.end_date,
                interval=self.time_interval,
                proxy=proxy,
            )
            temp_df["tic"] = tic
            self.dataframe = pd.concat([self.dataframe, temp_df], axis=0, join="outer")
        self.dataframe.reset_index(inplace=True)
        try:
            self.dataframe.columns = [
                "date",
                "open",
                "high",
                "low",
                "close",
                "adjusted_close",
                "volume",
                "tic",
            ]
        except NotImplementedError:
            print("the features are not supported currently")
        self.dataframe["day"] = self.dataframe["date"].dt.dayofweek
        self.dataframe["date"] = self.dataframe.date.apply(
            lambda x: x.strftime("%Y-%m-%d")
        )
        self.dataframe.dropna(inplace=True)
        self.dataframe.reset_index(drop=True, inplace=True)
        print("Shape of DataFrame: ", self.dataframe.shape)
        self.dataframe.sort_values(by=["date", "tic"], inplace=True)
        self.dataframe.reset_index(drop=True, inplace=True)
