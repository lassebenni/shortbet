import threading
import concurrent.futures
import time
import os
from typing import Generator

import yfinance as yf

from short_ticker import ShortTicker


thread_local = threading.local()


class ProcessTickers:
    def __init__(
        self,
        full_run: bool = False,
        symbols_path: str = "symbols.txt",
        history_path: str = "data/history.csv",
        latest_path: str = "data/latest.csv",
    ):
        self.full_run = full_run
        print(f"Full run? {full_run}")

        self.history_filename = history_path
        self.latest_filename = latest_path

        self.symbols = self._read_symbols(symbols_path)

    def run(self):
        start = time.time()
        first_symbol = next(self.symbols)
        self._store_first_symbol(first_symbol)

        if self.full_run == True:
            with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
                executor.map(self._store_ticker, self.symbols)

        self._print_duration(start, "extract_tickers")

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

    def _print_duration(self, start: float, action: str):
        duration = time.time() - start
        print(f"Duration was: {duration} for {action}")

    def _read_symbols(self, filename: str, buffer_size: int = 3) -> Generator:
        with open(filename, "rb") as file:
            chunk = file.readlines(buffer_size)
            while chunk:
                symbol = chunk[0].decode("utf-8").strip()
                yield symbol
                chunk = file.readlines(buffer_size)
