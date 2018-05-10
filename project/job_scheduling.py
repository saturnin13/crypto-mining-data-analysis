import threading
import time

from src.historical_data_fetcher.gpu_statistics.gpu_statistics_database_interactions import GpuStatisticsDatabaseInteractions
from src.historical_data_fetcher.historical_data.currencies_database_interactions import CurrenciesDatabaseInteractions
from src.live_data_fetcher.live_data_table_filling import LiveDataTableFilling
from src.variables.variables import Variables

# Check that the ubiq site is not own anymore https://ubiqscan.io/
class JobScheduling():

    def __init__(self):
        self.gpu_statistics_database_interactions = GpuStatisticsDatabaseInteractions()
        self.currencies_database_interactions = CurrenciesDatabaseInteractions()
        self.live_data_filling = LiveDataTableFilling()
        threading.Thread(target=self.recurrent_update_gpu).start()
        threading.Thread(target=self.recurrgitent_update_historical_data).start()
        threading.Thread(target=self.recurrent_update_live_data).start()

    def recurrent_update_gpu(self):
        self.__launch_periodically(self.gpu_statistics_database_interactions.update, Variables.GPU_STATISTICS_DATABASE_UPDATE_RATE / 1000, "updating gpu data")

    def recurrent_update_historical_data(self):
        self.__launch_periodically(self.currencies_database_interactions.update_all, Variables.CURRENCY_HISTORICAL_DATABASE_UPDATE_RATE / 1000, "updating historical data")

    def recurrent_update_live_data(self):
        self.__launch_periodically(self.live_data_filling.fill_all_tables, Variables.CURRENCY_LIVE_DATABASE_UPDATE_RATE / 1000, "updating live data")

    def __launch_periodically(self, func, timeout, action_msg):
        print("\nSTARTING " + action_msg.upper() + "\n")
        thread = threading.Thread(target=func)
        thread.start()
        thread.join()
        print("\nFINISHED " + action_msg.upper() + "\n")
        time.sleep(timeout)
        self.__launch_periodically(func, timeout, action_msg)


job_scheduling = JobScheduling()