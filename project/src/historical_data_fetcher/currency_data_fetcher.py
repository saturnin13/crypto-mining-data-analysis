import datetime
from time import sleep

from src.currencies.currencies import Currencies
from src.data_scrapper.blockchain_explorer.blockchain_explorer_data_scrapper_factory import DataScrapperFactory
from src.database_accessor.database_accessor import DatabaseAccessor

from src.printing.colors import Colors


class CurrencyDataFetcher:
    def __init__(self):
        pass

    def fill_database(self, currency, time_delta=datetime.timedelta(hours=1), sleep_time=1, block_number=1):
        data_scrapper = DataScrapperFactory.getDataScrapper(currency)
        db = DatabaseAccessor()
        block_under = -1
        block_number_incrementation = 1
        current_date_time = data_scrapper.get_block_date(block_number)
        datetime_limit = self.__initial_datetime_limit(time_delta, current_date_time)

        while(True):
            print("\nblock: " + str(block_number))
            current_date_time = data_scrapper.get_block_date(block_number)
            datetime_difference = self.__check_time_limit_frame(current_date_time, datetime_limit, time_delta)
            if(block_number == block_under + 1):
                datetime_limit = self.__initial_datetime_limit(time_delta, current_date_time)
                block_under = -1
            if(datetime_difference == -1):
                print("Date of current block (" + str(current_date_time) + ") is too small compared to the last one (" + str(datetime_limit) + ") and the delta(" + str(time_delta) + ")")
                block_under = block_number if block_number > block_under else block_under
                block_number_incrementation += 2
            elif(datetime_difference == 1):
                print("Date of current block (" + str(current_date_time) + ") is too big compared to the last one (" + str(datetime_limit) + ") and the delta (" + str(time_delta) + ")")
                block_number -= block_number_incrementation
                block_number_incrementation = min(int(0.9 * block_number_incrementation), 1)
            else:
                print(Colors.OKBLUE + "Processing block " + str(block_number) + ", retrieving the data" + Colors.ENDC)
                current_reward = data_scrapper.get_block_reward(block_number)
                current_difficulty = data_scrapper.get_block_difficulty(block_number)
                datetime_limit += time_delta
                db.upsert_currency_historical_data(currency, current_reward, current_difficulty, block_number, current_date_time, datetime_limit, datetime_limit + time_delta)
            block_number += block_number_incrementation
            sleep(sleep_time)


    def __check_time_limit_frame(self, current_date_time, time_limit, time_delta):
        if(time_limit > current_date_time):
            return -1
        elif(time_limit <= current_date_time and time_limit + time_delta >= current_date_time):
            return 0
        else:
            return 1

    def __initial_datetime_limit(self, time_delta, current_date_time):
        if(time_delta.days != 0):
            return datetime.datetime(current_date_time.year, current_date_time.month, current_date_time.day)
        elif (time_delta.seconds >= 3600):
            return datetime.datetime(current_date_time.year, current_date_time.month, current_date_time.day, current_date_time.hour)
        elif (time_delta.seconds >= 60):
            return datetime.datetime(current_date_time.year, current_date_time.month, current_date_time.day, current_date_time.hour, current_date_time.minute)
        elif (time_delta.seconds != 0):
            return datetime.datetime(current_date_time.year, current_date_time.month, current_date_time.day, current_date_time.hour, current_date_time.minute, current_date_time.second)


test = CurrencyDataFetcher()
test.fill_database(Currencies.GRS, sleep_time=2, block_number=1, time_delta=datetime.timedelta(seconds=30))

