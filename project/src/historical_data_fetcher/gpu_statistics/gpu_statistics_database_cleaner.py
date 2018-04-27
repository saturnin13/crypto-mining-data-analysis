from src.database_accessor.database_accessor import DatabaseAccessor


class GpuStatisticsDatabaseCleaner:
    def __init__(self):
        self.db = DatabaseAccessor()

    def clean(self):
        self.db.truncate_table("gpu_statistics")