import concurrent.futures
import json
import time
from typing import Generator, List

from model.short_ticker import ShortTicker

SYMBOLS_PATH = "symbols.txt"
LATEST_JSON_PATH = "data/latest.json"


class ProcessTickers:
    def __init__(
        self,
    ):
        self.symbols = self._read_symbols(SYMBOLS_PATH)
        self.existing_latest_tickers = self._read_tickers()
        self.latest_tickers: List[ShortTicker] = []

    def run(self, full_run: bool = False):
        start = time.time()
        first_symbol = next(self.symbols)
        self._store_first_symbol(first_symbol)

        if not full_run:
            print("Done processing.")
        else:
            print("Starting to process all symbols")
            with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
                executor.map(self._store_ticker, self.symbols)
            self._overwrite_tickers_file()

        self._print_duration(start, "extract_tickers")

    def _store_first_symbol(self, symbol: str):
        try:
            ticker = ShortTicker(symbol)
            self.latest_tickers.append(ticker)
            self._overwrite_tickers_file()
        except ValueError:
            print(f"Could not store {symbol}")

    def _store_ticker(self, symbol: str):
        try:
            ticker = ShortTicker(symbol)
            self.latest_tickers.append(ticker)
        except ValueError:
            print(f"Could not store {symbol}")

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

    def _read_tickers(self):
        with open(LATEST_JSON_PATH, "r") as file:
            return json.loads(file.read())

    def _update_tickers(self, filename: str):
        pass

    def _overwrite_tickers_file(self):
        with open(LATEST_JSON_PATH, "w") as file:
            tickers_json = [ticker.as_dict() for ticker in self.latest_tickers]
            json.dump(tickers_json, file, default=str)
