import datetime

from src.currencies.currencies import Currencies
from src.historical_data_fetcher.currency_database_filling import CurrencyDatabaseFilling


class GRSDatabaseFilling:
    def __init__(self):
        pass

    def fill(self):
        database_filler = CurrencyDatabaseFilling()
        database_filler.fill_in_database_for_currency(Currencies.GRS, sleep_time_blockchain=2, block_number=1, time_delta=datetime.timedelta(days=30))

grs = GRSDatabaseFilling()
grs.fill()