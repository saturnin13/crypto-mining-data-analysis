import datetime

from src.currencies.currencies import Currencies
from src.database_accessor.database_accessor import DatabaseAccessor
from src.historical_data_fetcher.historical_data.currency_historical_data_cleaner import CurrencyHistoricalDataDatabaseCleaner
from src.historical_data_fetcher.historical_data.currency_historical_data_database_filling import CurrencyHistoricalDataDatabaseFilling


class CurrenciesDatabaseInteractions:
    def __init__(self):
        self.database_filling = CurrencyHistoricalDataDatabaseFilling()
        self.database_cleaner = CurrencyHistoricalDataDatabaseCleaner()

    def update_all(self):
        self.update([item for item in Currencies])

    def update(self, currencies, time_delta=datetime.timedelta(days=1)):
        if (type(currencies) != list):
            currencies = [currencies]
        for currency in currencies:
            most_recent_valid_row = DatabaseAccessor.get_most_recent_valid_row_currency_database(currency)
            if(most_recent_valid_row):
                self.__load_helper(currency, time_delta=time_delta, block_number=most_recent_valid_row["block_number"], datetime_lower_limit_value=most_recent_valid_row["datetime"])
            else:
                self.load(currency, time_delta)

    def clean_and_reload(self, currencies, time_delta=datetime.timedelta(days=1)):
        if (type(currencies) != list):
            currencies = [currencies]
        self.database_cleaner.clean(currencies)
        self.load(currencies, time_delta)

    def load(self, currencies, time_delta=datetime.timedelta(days=1)):
        if(type(currencies) != list):
            currencies = [currencies]
        for currency in currencies:
            self.__load_helper(currency, time_delta=time_delta)

    def __load_helper(self, currency, time_delta=datetime.timedelta(days=1), block_number=1, datetime_lower_limit_value=None):
        self.database_filling.fill_in_database_for_currency(currency, block_number=block_number, time_delta=time_delta,
                                                            datetime_lower_limit_value=datetime_lower_limit_value)