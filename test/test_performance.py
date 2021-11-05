import time

import process_tickers as pts


def test_process_tickers_performance(tmpdir):
    """
    Test the performance of the ProcessTickers function.
    """

    hist_path = tmpdir.join("history.csv")
    latest_path = tmpdir.join("latest.csv")

    pt = pts.ProcessTickers(
        history_path=hist_path,
        latest_path=latest_path,
    )

    # Test the performance of the ProcessTickers function
    start = time.time()
    pt.run()
    duration = time.time() - start
    assert duration < 10
