import datetime

from src.currencies.currencies import Currencies
from src.historical_data_fetcher.historical_data.currency_historical_data_database_filling import CurrencyHistoricalDataDatabaseFilling


class GRSDatabaseFilling:
    def __init__(self):
        pass

    def fill(self):
        database_filler = CurrencyHistoricalDataDatabaseFilling()
        database_filler.fill_in_database_for_currency(Currencies.GRS, sleep_time_blockchain=2, block_number=2056770, time_delta=datetime.timedelta(days=1))

grs = GRSDatabaseFilling()
grs.fill()