from dataclasses import dataclass
from typing import List

import fire
import yfinance as yf
from pandas import Timestamp


@dataclass
class ShortTicker:
    earnings_date: Timestamp
    name: str
    short_float: float
    ticker: str

    def __init__(self, ticker: yf.Ticker):
        self.name = ticker.info.get("shortName", "")
        self.short_float = round(ticker.info.get("sharesPercentSharesOut", 0) * 100, 2)
        self.ticker = ticker.ticker
        if ticker.calendar is not None and not ticker.calendar.empty:
            self.earnings_date = ticker.calendar.iloc[0][0]

    def print(self):
        print(f"{self.ticker} {self.name} {self.short_float} {self.earnings_date}")


def get_ticker(symbol: str) -> yf.Ticker:
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


def parse_symbols(filename: str) -> List:
    res = []
    with open(filename, "r") as file:
        text = file.read()
        res = [x.rstrip().lstrip() for x in text.split("\n") if x]
    return res


def ticker():
    symbols = parse_symbols("symbols.txt")
    tickers: List[ShortTicker] = [get_ticker(x) for x in symbols]
    for ticker in tickers:
        ticker.print()
        with open("data/results.txt", "a") as f:
            f.write(
                f"{ticker.ticker} {ticker.name} {ticker.short_float} {ticker.earnings_date}\n"
            )


if __name__ == "__main__":
    fire.Fire(ticker)
