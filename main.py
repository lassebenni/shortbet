import os

from process_tickers import ProcessTickers

if __name__ == "__main__":
    full_run = bool(os.environ.get("FULL_RUN", False))

    process_tickers = ProcessTickers(full_run)
    process_tickers.run()
