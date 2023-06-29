from concurrent.futures import ThreadPoolExecutor
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
        self.parallel = True
        self.symbols = self._read_symbols(SYMBOLS_PATH)

    def run(self, full_run: bool = False):
        start = time.time()
        first_symbol = next(self.symbols)
        self._store_ticker(first_symbol)

        if not full_run:
            print("Done processing.")
        else:
            print("Starting to process all symbols")
            if self.parallel:
                with ThreadPoolExecutor(max_workers=100) as executor:
                    executor.map(self._store_ticker, self.symbols)
            else:
                for symbol in self.symbols:
                    self._store_ticker(symbol)

        self._print_duration(start, "extract_tickers")

    def _store_ticker(self, symbol: str):
        try:
            print("storing ticker")
            ticker = ShortTicker(symbol)
            with open(LATEST_JSON_PATH, "a") as file:
                json.dump(ticker.as_dict(), file, default=str)
                file.write('\n')
        except Exception as e:
            print(f"Could not store {symbol}: {e}")


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

