from dataclasses import dataclass
from datetime import datetime, date

from dataclass_csv import DataclassWriter
import yfinance as yf


@dataclass
class ShortTicker:
    earnings_date: str = ""
    name: str = ""
    short_float: float = 0
    ticker: str = ""
    datetime: date = datetime.now().date()

    def __init__(self, ticker: yf.Ticker):
        if ticker is None:
            raise ValueError("Ticker must not be None")

        if ticker.calendar is not None and not ticker.calendar.empty:
            self.earnings_date = datetime.strftime(
                ticker.calendar.iloc[0][0], "%Y-%m-%d"
            )

        if ticker.info:
            self.name = ticker.info.get("shortName", "")
            short_percentage = ticker.info.get("sharesPercentSharesOut")
            self.ticker = ticker.ticker

            if short_percentage:
                self.short_float = round(short_percentage * 100, 2)

    def to_csv(self, filename: str, skip_header: bool = False, append: bool = True):
        mode = "a" if append else "w"
        with open(filename, mode) as f:
            w = DataclassWriter(f, [self], ShortTicker)
            w.write(skip_header)

    def print(self):
        print(f"{self.ticker} {self.name} {self.short_float} {self.earnings_date}")
