from dataclasses import dataclass, asdict as _asdict
from datetime import datetime, date
import json

import pandas as pd
from dataclass_csv import DataclassWriter
import yfinance as yf
import numpy as np


@dataclass
class ShortTicker:
    earnings_date: str = ""
    name: str = ""
    short_float: float = 0
    price: float = 0
    symbol: str = ""
    datetime: date = datetime.now().date()
    url: str = ""

    def __init__(self, symbol: str = ""):
        print(symbol)
        self.url = f"https://finance.yahoo.com/quote/{symbol}/"

        ticker = self._retrieve_yf_ticker(symbol)
        self.symbol = ticker.ticker

        if ticker.earnings_dates is not None and not ticker.earnings_dates.empty:
            self.get_first_future_earnings_date(ticker.earnings_dates)

        if ticker.info:
            self.name = ticker.info.get("shortName", "")
            self.price = ticker.info.get("currentPrice", "")
            short_percentage = ticker.info.get("sharesPercentSharesOut")
            if short_percentage:
                self.short_float = self._extract_short_float(short_percentage)

    def get_first_future_earnings_date(self, df_dates: pd.DataFrame):
            now = datetime.now()
            earnings_dates = df_dates.index.values
            future_datetimes = earnings_dates[earnings_dates > np.datetime64(now)]

            if len(future_datetimes) == 0:
                print("No future earnings date found.")
                self.earnings_date = ""
            else:
                closest_future_earnings_date = future_datetimes.min()
                self.earnings_date = closest_future_earnings_date.astype('datetime64[D]')

    def _retrieve_yf_ticker(self, symbol: str):
        ticker = yf.Ticker(symbol)

        if ticker:
            return ticker
        else:
            raise ValueError(f"Ticker {symbol} not found")

    def _extract_short_float(self, short_percentage: float):
        return round(short_percentage * 100, 2)

    def to_csv(self, filename: str, skip_header: bool = False, append: bool = True):
        mode = "a" if append else "w"
        with open(filename, mode) as f:
            w = DataclassWriter(f, [self], ShortTicker)
            w.write(skip_header)

    def to_json(self):
        return json.dumps(_asdict(self), sort_keys=True, default=str)

    def as_dict(self):
        return _asdict(self)

    def print(self):
        print(f"{self.symbol} {self.name} {self.short_float} {self.earnings_date}")
