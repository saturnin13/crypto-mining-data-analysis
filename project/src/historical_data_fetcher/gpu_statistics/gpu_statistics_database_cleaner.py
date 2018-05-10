from src.database_accessor.database_accessor import DatabaseAccessor


class GpuStatisticsDatabaseCleaner:

    def clean(self):
        DatabaseAccessor.truncate_table("gpu_statistics")