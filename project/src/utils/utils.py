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

    @staticmethod
    def smoothen_up_data(data, smoothness_value):
        result = []
        for i in range(len(data)):
            min_value = max(i - smoothness_value, 0)
            max_value = min(len(data) - 1, i + smoothness_value)
            result.append(sum(data[min_value:max_value]) / (max_value - min_value))
        return result

    @staticmethod
    def remove_spikes(data, multiple=5, distance_from_point=3):
        data = list(data)
        for i in range(len(data)):
            for j in range(2 * distance_from_point + 1):
                index = i + j - distance_from_point
                if (index >= 0 and index < len(data) and data[i] > data[index] * multiple):
                    data[i] = data[index]
                    continue

            if(i + distance_from_point < len(data) and i - distance_from_point >= 0):
                if(data[i] > data[i + 1] * multiple or data[i] > data[i - 1] * multiple):
                    data[i] = (data[i - 1] + data[i + 1]) / 2

        return data

