import time, threading

from src.currencies.currencies import Currencies
from src.historical_data_fetcher.gpu_statistics.gpu_statistics_database_interactions import GpuStatisticsDatabaseInteractions
from src.historical_data_fetcher.historical_data.currencies_database_interactions import CurrenciesDatabaseInteractions
from src.live_data_fetcher.live_data_table_filling import LiveDataTableFilling
from src.variables.variables import Variables


class JobScheduling():

    def __init__(self):
        self.gpu_statistics_database_interactions = GpuStatisticsDatabaseInteractions()
        self.currencies_database_interactions = CurrenciesDatabaseInteractions()
        self.live_data_filling = LiveDataTableFilling()
        self.recurrent_update_gpu()
        self.recurrent_update_historical_data()
        self.recurrent_update_live_data()

    def recurrent_update_gpu(self):
        self.gpu_statistics_database_interactions.update()
        threading.Timer(Variables.GPU_STATISTICS_DATABASE_UPDATE_RATE / 1000, self.recurrent_update_gpu).start()

    def recurrent_update_historical_data(self):
        self.currencies_database_interactions.update([item for item in Currencies])
        threading.Timer(Variables.CURRENCY_HISTORICAL_DATABASE_UPDATE_RATE / 1000, self.recurrent_update_historical_data).start()

    def recurrent_update_live_data(self):
        self.live_data_filling.fill_all_tables()
        threading.Timer(Variables.CURRENCY_LIVE_DATABASE_UPDATE_RATE / 1000, self.recurrent_update_live_data).start()


job_scheduling = JobScheduling()


