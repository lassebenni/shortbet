import time
import pytest
import pandas as pd

import process_tickers as pts
from process_tickers import ShortTicker, SYMBOLS_PATH, LATEST_JSON_PATH


class FakeTicker:
    def __init__(self):
        self.ticker = "FAKE"
        self.calendar = pd.DataFrame({"Date": [pd.Timestamp(0)]})
        self.info = {"shortName": "Fake Tick", "sharesPercentSharesOut": 0.28}


def return_delayed_fake_ticker(s, x):
    time.sleep(5)
    return FakeTicker()
