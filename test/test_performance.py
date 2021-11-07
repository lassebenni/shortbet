import time
import pytest
import pandas as pd

import process_tickers as pts
from process_tickers import ShortTicker


class FakeTicker:
    def __init__(self):
        self.ticker = "FAKE"
        self.calendar = pd.DataFrame({"Date": [pd.Timestamp(0)]})
        self.info = {"shortName": "Fake Tick", "sharesPercentSharesOut": 0.28}


def return_delayed_fake_ticker(s, x):
    time.sleep(5)
    return FakeTicker()


@pytest.mark.parametrize(
    "full_run, multi_process, expected_duration",
    [(False, False, 10), (True, True, 15), (True, False, 60)],
)
def test_process_tickers_performance(
    tmpdir, full_run, multi_process, expected_duration
):
    """
    Test the performance of the ProcessTickers function.
    """

    # override networking call
    ShortTicker._retrieve_yf_ticker = return_delayed_fake_ticker

    hist_path = tmpdir.join("history.csv")
    latest_path = tmpdir.join("latest.csv")

    pt = pts.ProcessTickers(
        symbols_path="test/test_symbols.txt",
        history_path=hist_path,
        latest_path=latest_path,
    )

    # Test the performance of the ProcessTickers function
    start = time.time()
    pt.run(full_run, multi_process)
    duration = time.time() - start
    print(duration)
    assert duration < expected_duration
