from src.database_accessor.database_accessor import DatabaseAccessor


class CurrencyHistoricalDataDatabaseCleaner:

    def clean(self, currencies):
        for currency in currencies:
            DatabaseAccessor.truncate_table(currency + "_historical_data")