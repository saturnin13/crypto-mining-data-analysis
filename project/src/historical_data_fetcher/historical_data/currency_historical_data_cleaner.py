from src.database_accessor.database_accessor import DatabaseAccessor


class CurrencyHistoricalDataDatabaseCleaner:
    def __init__(self):
        self.db = DatabaseAccessor()

    def clean(self, currencies):
        for currency in currencies:
            self.db.truncate_table(currency + "_historical_data")