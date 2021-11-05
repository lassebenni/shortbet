import concurrent.futures
import threading
from dataclasses import dataclass
from datetime import datetime, date
from typing import List, Generator
import os

from dataclass_csv import DataclassWriter
import yfinance as yf
import time

FULL_RUN = bool(os.environ.get("FULL_RUN", True))
WORKER_COUNT = 100

thread_local = threading.local()


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


def read_symbols(filename: str, buffer_size: int = 3) -> Generator:
    with open(filename, "rb") as file:
        chunk = file.readlines(buffer_size)
        while chunk:
            symbol = chunk[0].decode("utf-8").strip()
            yield symbol
            chunk = file.readlines(buffer_size)


def store_ticker(symbol: str):
    ticker = get_short_ticker(symbol)
    if ticker.earnings_date:
        ticker.to_csv("data/results.csv", skip_header=True)
        ticker.to_csv("data/history.csv", skip_header=True)
        ticker.print()


def extract_tickers():
    symbols_generator = read_symbols("symbols.txt")

    first_symbol = next(symbols_generator)
    first_ticker = get_short_ticker(first_symbol)
    first_ticker.to_csv("data/results.csv", skip_header=False, append=False)

    if FULL_RUN == True:
        with concurrent.futures.ThreadPoolExecutor(
            max_workers=WORKER_COUNT
        ) as executor:
            executor.map(store_ticker, symbols_generator)


def print_duration(start: float, action: str):
    duration = time.time() - start
    print(f"Duration was: {duration} for {action}")


if __name__ == "__main__":
    start_time = time.time()
    print(f"Full run? {FULL_RUN}")

    extract_tickers()
    print_duration(start_time, "extract_tickers")
