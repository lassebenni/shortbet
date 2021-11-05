import concurrent.futures
import time
from typing import Generator

from short_ticker import ShortTicker


class ProcessTickers:
    def __init__(
        self,
        symbols_path: str = "symbols.txt",
        history_path: str = "data/history.csv",
        latest_path: str = "data/latest.csv",
    ):

        self.history_filename = history_path
        self.latest_filename = latest_path

        self.symbols = self._read_symbols(symbols_path)

    def run(self, full_run: bool = False):
        start = time.time()
        first_symbol = next(self.symbols)
        self._store_first_symbol(first_symbol)

        if full_run:
            print("Processing all symbols")
            with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
                executor.map(self._store_ticker, self.symbols)

        self._print_duration(start, "extract_tickers")

    def _store_first_symbol(self, symbol: str):
        ticker = ShortTicker(symbol)
        ticker.to_csv(self.latest_filename, skip_header=False, append=False)

    def _store_ticker(self, symbol: str):
        ticker = ShortTicker(symbol)
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
