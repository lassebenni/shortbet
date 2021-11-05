from process_tickers import set_global_symbols, ProcessTickers


if __name__ == "__main__":
    set_global_symbols()
    process_tickers = ProcessTickers()
    process_tickers.run()
