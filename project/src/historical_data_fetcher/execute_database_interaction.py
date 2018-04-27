from src.currencies.currencies import Currencies
from src.historical_data_fetcher.gpu_statistics.gpu_statistics_database_interactions import GpuStatisticsDatabaseInteractions
from src.historical_data_fetcher.historical_data.currencies_database_interactions import CurrenciesDatabaseInteractions



# gpu_statistics_database_interactions = GpuStatisticsDatabaseInteractions()
# gpu_statistics_database_interactions.load()

grs = CurrenciesDatabaseInteractions()
grs.update([currency for currency in Currencies])

