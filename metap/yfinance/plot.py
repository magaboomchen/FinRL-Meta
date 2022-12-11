from finrl.meta.preprocessor.yahoodownloader import YahooDownloader


def get_baseline(ticker, start, end, proxy):
    return YahooDownloader(
        start_date=start, end_date=end, ticker_list=[ticker]
    ).fetch_data(proxy=proxy)
