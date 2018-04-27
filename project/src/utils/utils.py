import datetime


class Utils:
    @staticmethod
    def truncate_datetime_limit(time_delta, current_date_time):
        if (time_delta.total_seconds() >= 3600 * 24 * 30):
            return datetime.datetime(current_date_time.year, current_date_time.month, 1)
        elif(time_delta.total_seconds() >= 3600 * 24):
            return datetime.datetime(current_date_time.year, current_date_time.month, current_date_time.day)
        elif (time_delta.total_seconds() >= 3600):
            return datetime.datetime(current_date_time.year, current_date_time.month, current_date_time.day, current_date_time.hour)
        elif (time_delta.total_seconds() >= 60):
            return datetime.datetime(current_date_time.year, current_date_time.month, current_date_time.day, current_date_time.hour, current_date_time.minute)
        else:
            return datetime.datetime(current_date_time.year, current_date_time.month, current_date_time.day, current_date_time.hour, current_date_time.minute, current_date_time.second)