import datetime

from src.currencies.currencies import Currencies
from src.historical_data_fetcher.historical_data.currency_historical_data_database_filling import CurrencyHistoricalDataDatabaseFilling


class CurrenciesDatabaseFilling:
    def __init__(self):
        pass

    def fill(self):
        database_filler = CurrencyHistoricalDataDatabaseFilling()
        database_filler.fill_in_database_for_currency(Currencies.ETH, sleep_time_blockchain=0.01, block_number=1, time_delta=datetime.timedelta(days=1))
        # database_filler.fill_in_database_for_currency(Currencies.GRS, sleep_time_blockchain=2, block_number=2056770, time_delta=datetime.timedelta(days=1))

grs = CurrenciesDatabaseFilling()
grs.fill()