import time
import process_tickers as pts


def test_process_tickers_performance(tmpdir):
    """
    Test the performance of the ProcessTickers function.
    """

    # global symbols has to be overriden first
    pts.symbols = pts.read_symbols("test/test_symbols.txt")
    pts.set_global_symbols()

    # Create a ProcessTickers object
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
    print(duration)
    assert duration < 100
