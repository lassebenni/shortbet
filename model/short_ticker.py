from dataclasses import dataclass, asdict as _asdict
from datetime import datetime, date
import json

import pandas as pd
from dataclass_csv import DataclassWriter
import yfinance as yf


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

        if ticker.calendar is not None and not ticker.calendar.empty:
            earnings_date = ticker.calendar.iloc[0][0]
            if earnings_date:
                self.earnings_date = self._transform_earnings_date(earnings_date)

        if ticker.info:
            self.name = ticker.info.get("shortName", "")
            self.price = ticker.info.get("currentPrice", "")
            short_percentage = ticker.info.get("sharesPercentSharesOut")
            if short_percentage:
                self.short_float = self._extract_short_float(short_percentage)

    def _retrieve_yf_ticker(self, symbol: str):
        ticker = yf.Ticker(symbol)

        if ticker:
            return ticker
        else:
            raise ValueError(f"Ticker {symbol} not found")

    def _transform_earnings_date(self, earnings_date: pd.Timestamp):
        return datetime.strftime(earnings_date, "%Y-%m-%d")

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
