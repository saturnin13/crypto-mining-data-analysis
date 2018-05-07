from src.currencies.currencies import Currencies
from src.historical_data_fetcher.gpu_statistics.gpu_statistics_database_interactions import GpuStatisticsDatabaseInteractions
from src.historical_data_fetcher.historical_data.currencies_database_interactions import CurrenciesDatabaseInteractions

currencies_database_interactions = CurrenciesDatabaseInteractions()
currencies_database_interactions.update([item for item in Currencies])
