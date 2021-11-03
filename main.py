from dataclasses import dataclass
from datetime import datetime
from typing import List, Generator
import os

from dataclass_csv import DataclassWriter
from pandas import Timestamp
import yfinance as yf

FULL_RUN = os.environ.get("FULL_RUN")
print(f"Full run? {FULL_RUN}")


@dataclass
class ShortTicker:
    earnings_date: str = ""
    name: str = ""
    short_float: float = 0
    ticker: str = ""

    def __init__(self, ticker: yf.Ticker):
        if ticker.info:
            self.name = ticker.info.get("shortName", "")
            self.short_float = round(
                ticker.info.get("sharesPercentSharesOut", 0) * 100, 2
            )
            self.ticker = ticker.ticker

        if ticker.calendar is not None and not ticker.calendar.empty:
            self.earnings_date = datetime.strftime(
                ticker.calendar.iloc[0][0], "%Y-%m-%d"
            )

    def print(self):
        print(f"{self.ticker} {self.name} {self.short_float} {self.earnings_date}")


def get_short_ticker(symbol: str) -> ShortTicker:
    """
    Get ticker data from yfinance
    :param ticker: ticker symbol
    :return: yfinance ticker object
    """
    ticker = yf.Ticker(symbol)
    if ticker:
        return ShortTicker(ticker)
    else:
        raise ValueError(f"Ticker {symbol} not found")


def read_lines(filename: str, buffer_size: int = 3) -> Generator:
    file = open(filename, "rb")
    tmp_lines = file.readlines(buffer_size)
    while tmp_lines:
        yield tmp_lines
        tmp_lines = file.readlines(buffer_size)
    file.close()


def write_to_file(filename: str, ticker: ShortTicker):
    with open(filename, "a") as f:
        w = DataclassWriter(f, [ticker], ShortTicker)
        w.write()


def extract_tickers():
    for line in read_lines("symbols.txt"):
        symbol = line[0].decode("utf-8").strip()
        ticker = get_short_ticker(symbol)
        if ticker.earnings_date:
            write_to_file("data/results.csv", ticker)
            ticker.print()

        if not FULL_RUN == True:
            break


if __name__ == "__main__":
    extract_tickers()
