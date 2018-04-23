import datetime
from time import sleep

from src.data_scrapper.blockchain_explorer.blockchain_data_scrapper_factory import BlockChainDataScrapperFactory
from src.data_scrapper.exchange_rate.exchange_rate_data_scrapper_factory import \
    ExchangeRateDataScrapperFactory
from src.database_accessor.database_accessor import DatabaseAccessor
from src.historical_data_fetcher.historical_data.currency_historical_data_revenue_calculator import HistoricalDataRevenueCalculator
from src.printing.colors import Colors


class CurrencyHistoricalDataDatabaseFilling:
    def __init__(self):
        self.db = DatabaseAccessor()

    def fill_in_database_for_currency(self, currency, time_delta=datetime.timedelta(hours=1), sleep_time_blockchain=1, sleep_time_exchange_rate=1, block_number=1):
        self.__fill_in_blockchain_data(currency, time_delta, sleep_time_blockchain, block_number)
        self.__fill_in_exchange_rate_data(currency, time_delta)
        self.__fill_in_revenue_data(currency)

    def __fill_in_blockchain_data(self, currency, time_delta, sleep_time_blockchain, block_number):
        data_scrapper = BlockChainDataScrapperFactory.getDataScrapper(currency)
        highest_block_under_datetime_range = -1
        block_number_incrementation = 1
        data = data_scrapper.get_data({"block_number": [block_number]})
        current_date_time = data[0]["datetime"]
        datetime_lower_limit = self.__truncated_datetime_limit(time_delta, current_date_time)

        while(True):
            print("\nblock: " + str(block_number))
            data = data_scrapper.get_data({"block_number": [block_number]})
            if(not data):
                break
            current_date_time = data[0]["datetime"]
            datetime_difference = self.__check_time_limit_frame(current_date_time, datetime_lower_limit, time_delta)
            if(block_number == highest_block_under_datetime_range + 1):
                datetime_lower_limit = self.__truncated_datetime_limit(time_delta, current_date_time)
            if(datetime_difference == -1):
                print("Date of current block (" + str(current_date_time) + ") is too small compared to the last one (" + str(datetime_lower_limit) + ") and the delta(" + str(time_delta) + ")")
                highest_block_under_datetime_range = block_number if block_number > highest_block_under_datetime_range else highest_block_under_datetime_range
                block_number_incrementation = int(2 * block_number_incrementation + 1) # worked with 2 before
            elif(datetime_difference == 1):
                print("Date of current block (" + str(current_date_time) + ") is too big compared to the last one (" + str(datetime_lower_limit) + ") and the delta (" + str(time_delta) + ")")
                block_number -= block_number_incrementation
                block_number_incrementation = max(int(0.9 * block_number_incrementation), 1)
            else:
                print(Colors.OKBLUE + "Processing block " + str(block_number) + ", retrieving the data" + Colors.ENDC)
                current_reward = data[0]["block_reward"]
                current_difficulty = data[0]["difficulty"]
                self.db.upsert_currency_blockchain_historical_data(currency, current_reward, current_difficulty, block_number,
                                                              self.__truncated_datetime_limit(time_delta, current_date_time),
                                                              datetime_lower_limit, datetime_lower_limit + time_delta)
                datetime_lower_limit += time_delta
            block_number += block_number_incrementation
            sleep(sleep_time_blockchain)

    def __fill_in_exchange_rate_data(self, currency, time_delta):
        data_scrapper = ExchangeRateDataScrapperFactory.getDataScrapper(currency)
        closes_exchange_rates = data_scrapper.get_data()
        datetime_lower_limit = self.__truncated_datetime_limit(time_delta, closes_exchange_rates[0]["datetime"])

        for i in range(len(closes_exchange_rates)):
            current_date_time = closes_exchange_rates[i]["datetime"]
            datetime_difference = self.__check_time_limit_frame(current_date_time, datetime_lower_limit, time_delta)
            if(datetime_difference == -1):
                pass
            elif(datetime_difference == 1):
                datetime_lower_limit = self.__truncated_datetime_limit(time_delta, current_date_time)
                i -= 1
            else:
                close_value = closes_exchange_rates[i]["close"]
                self.db.upsert_currency_exchange_rate_historical_data(currency, close_value, self.__truncated_datetime_limit(time_delta, current_date_time),
                                                                      datetime_lower_limit, datetime_lower_limit + time_delta)
                datetime_lower_limit += time_delta

    def __fill_in_revenue_data(self, currency):
        revenue_calculator = HistoricalDataRevenueCalculator()
        revenues_and_datetime = revenue_calculator.get_currency_historic_revenue(currency)
        for row in revenues_and_datetime:
            revenue = row[0]
            date_time = row[1]
            self.db.update_revenue_historical_data_currrencies(currency, revenue, date_time)


    def __check_time_limit_frame(self, current_date_time, time_limit, time_delta):
        if(time_limit > current_date_time):
            return -1
        elif(time_limit <= current_date_time and time_limit + time_delta > current_date_time):
            return 0
        else:
            return 1

    def __truncated_datetime_limit(self, time_delta, current_date_time):
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

