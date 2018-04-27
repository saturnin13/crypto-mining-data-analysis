from src.historical_data_fetcher.gpu_statistics.gpu_statistics_database_cleaner import GpuStatisticsDatabaseCleaner
from src.historical_data_fetcher.gpu_statistics.gpu_statistics_database_filling import GpuStatisticsDatabaseFilling


class GpuStatisticsDatabaseInteractions:
    def __init__(self):
        self.database_filling = GpuStatisticsDatabaseFilling()
        self.database_cleaner = GpuStatisticsDatabaseCleaner()

    def update(self):
        self.load()

    def clean_and_reload(self):
        self.database_cleaner.clean()
        self.load()

    def load(self):
        self.database_filling.fill_in_database()