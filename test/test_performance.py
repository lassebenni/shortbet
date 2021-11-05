import time
import pytest

import process_tickers as pts


@pytest.mark.parametrize("full_run, expected_duration", [(False, 5), (True, 30)])
def test_process_tickers_performance(tmpdir, full_run, expected_duration):
    """
    Test the performance of the ProcessTickers function.
    """

    hist_path = tmpdir.join("history.csv")
    latest_path = tmpdir.join("latest.csv")

    pt = pts.ProcessTickers(
        symbols_path="test/test_symbols.txt",
        history_path=hist_path,
        latest_path=latest_path,
    )

    # Test the performance of the ProcessTickers function
    start = time.time()
    pt.run(full_run)
    duration = time.time() - start
    print(duration)
    assert duration < expected_duration
