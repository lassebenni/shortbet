import time
import os
from typing import Generator

import multiprocessing
import yfinance as yf

from short_ticker import ShortTicker

FULL_RUN = bool(os.environ.get("FULL_RUN", True))

symbols = None


def set_global_symbols():
    global symbols
    if not symbols:
        symbols = read_symbols("symbols.txt")


def read_symbols(filename: str, buffer_size: int = 3) -> Generator:
    with open(filename, "rb") as file:
        chunk = file.readlines(buffer_size)
        while chunk:
            symbol = chunk[0].decode("utf-8").strip()
            yield symbol
            chunk = file.readlines(buffer_size)


class ProcessTickers:
    def __init__(
        self,
        history_path: str = "data/history.csv",
        latest_path: str = "data/latest.csv",
    ):
        self.history_filename = history_path
        self.latest_filename = latest_path

    def run(self):
        start = time.time()
        first_symbol = next(symbols)
        self._store_first_symbol(first_symbol)

        print(f"Full run? {FULL_RUN}")
        if FULL_RUN == True:
            with multiprocessing.Pool(initializer=set_global_symbols) as pool:
                pool.map(self._store_ticker, symbols)

        self.print_duration(start, "extract_tickers")

    def _store_first_symbol(self, symbol: str):
        ticker = self._get_short_ticker(symbol)
        ticker.to_csv(self.latest_filename, skip_header=False, append=False)

    def _get_short_ticker(self, symbol: str) -> ShortTicker:
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

    def _store_ticker(self, symbol: str):
        ticker = self._get_short_ticker(symbol)
        if ticker.earnings_date:
            ticker.to_csv(self.latest_filename, skip_header=True)
            ticker.to_csv(self.history_filename, skip_header=True)
            ticker.print()

    def print_duration(self, start: float, action: str):
        duration = time.time() - start
        print(f"Duration was: {duration} for {action}")
