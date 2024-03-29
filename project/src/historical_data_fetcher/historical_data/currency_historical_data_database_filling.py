import datetime

from src.data_scrapper.blockchain_explorer.blockchain_data_scrapper_factory import BlockChainDataScrapperFactory
from src.data_scrapper.exchange_rate.exchange_rate_data_scrapper_factory import \
    ExchangeRateDataScrapperFactory
from src.database_accessor.database_accessor import DatabaseAccessor
from src.historical_data_fetcher.historical_data.currency_historical_data_revenue_calculator import HistoricalDataRevenueCalculator
from src.printing.colors import Colors
from src.utils.utils import Utils


class CurrencyHistoricalDataDatabaseFilling:

    def fill_in_database_for_currency(self, currency, time_delta=datetime.timedelta(hours=1), block_number=1, datetime_lower_limit_value=None):
        self.data_analysis_module__third_parties(currency, time_delta, block_number)
        self.__fill_in_exchange_rate_data(currency, time_delta, datetime_lower_limit_value=datetime_lower_limit_value)
        self.__fill_in_revenue_data(currency, datetime_lower_limit_value=datetime_lower_limit_value)

    def __fill_in_blockchain_data(self, currency, time_delta, block_number):
        block_number = block_number if(currency.starting_block() < block_number) else currency.starting_block()

        data_scrapper = BlockChainDataScrapperFactory.getDataScrapper(currency)
        highest_block_under_datetime_range = -1
        block_number_incrementation = 1
        data = data_scrapper.get_data({"block_number": [block_number]})
        if(not data):
            print("Could not find the initial block for " + str(currency) + " and block number " + str(block_number) + ", exiting the __fill_in_blockchain_data function")
            return
        current_date_time = data[0]["datetime"]
        datetime_lower_limit = Utils.truncate_datetime_limit(time_delta, current_date_time)

        while(True):
            print("\nBlock: " + str(block_number) + " for currency: " + str(currency))
            data = data_scrapper.get_data_with_sleep({"block_number": [block_number]})
            if(not data):
                break
            current_date_time = data[0]["datetime"]
            datetime_difference = self.__check_time_limit_frame(current_date_time, datetime_lower_limit, time_delta)
            if(block_number == highest_block_under_datetime_range + 1):
                datetime_lower_limit = Utils.truncate_datetime_limit(time_delta, current_date_time)
            if(datetime_difference == -1):
                print("Date of current block (" + str(current_date_time) + ") is too small compared to the last one (" + str(datetime_lower_limit) + ") and the delta(" + str(time_delta) + ")")
                highest_block_under_datetime_range = block_number if block_number > highest_block_under_datetime_range else highest_block_under_datetime_range
                block_number_incrementation = int(2 * block_number_incrementation + 1) # worked with 2 before
            elif(datetime_difference == 1):
                print("Date of current block (" + str(current_date_time) + ") is too big compared to the last one (" + str(datetime_lower_limit) + ") and the delta (" + str(time_delta) + ")")
                block_number -= block_number_incrementation
                block_number_incrementation = max(int(0.8 * block_number_incrementation), 1)
            else:
                print(Colors.WARNING + "Processing block " + str(block_number) + ", retrieving the data" + Colors.ENDC)
                highest_block_under_datetime_range = block_number if block_number > highest_block_under_datetime_range else highest_block_under_datetime_range
                current_reward = data[0]["reward"]
                current_difficulty = data[0]["difficulty"]
                DatabaseAccessor.upsert_currency_blockchain_historical_data(currency, current_reward, current_difficulty, block_number,
                                                                   Utils.truncate_datetime_limit(time_delta, current_date_time),
                                                                   datetime_lower_limit, datetime_lower_limit + time_delta)
                datetime_lower_limit += time_delta
            block_number += block_number_incrementation

    def __fill_in_exchange_rate_data(self, currency, time_delta, datetime_lower_limit_value=None):
        data_scrapper = ExchangeRateDataScrapperFactory.getDataScrapper(currency)
        closes_exchange_rates = data_scrapper.get_data()
        if(not closes_exchange_rates):
            print("Could not find the closes exchange rate for " + str(currency) + ", exiting the __fill_in_blockchain_data function")
        datetime_lower_limit_value = closes_exchange_rates[0]["datetime"] if datetime_lower_limit_value is None else datetime_lower_limit_value
        datetime_lower_limit = Utils.truncate_datetime_limit(time_delta, datetime_lower_limit_value)

        i = 0
        while(i < len(closes_exchange_rates)):
            current_date_time = closes_exchange_rates[i]["datetime"]
            datetime_difference = self.__check_time_limit_frame(current_date_time, datetime_lower_limit, time_delta)
            if(datetime_difference == -1):
                pass
            elif(datetime_difference == 1):
                datetime_lower_limit = Utils.truncate_datetime_limit(time_delta, current_date_time)
                i -= 1
            else:
                close_value = closes_exchange_rates[i]["close"]
                DatabaseAccessor.upsert_currency_exchange_rate_historical_data(currency, close_value, Utils.truncate_datetime_limit(time_delta, current_date_time),
                                                                      datetime_lower_limit, datetime_lower_limit + time_delta)
                datetime_lower_limit += time_delta
            i += 1

    def __fill_in_revenue_data(self, currency, datetime_lower_limit_value=None):
        revenue_calculator = HistoricalDataRevenueCalculator()
        revenues_and_datetime = revenue_calculator.get_currency_historic_revenue(currency)
        datetime_lower_limit_value = datetime.datetime(1970, 1, 1) if datetime_lower_limit_value is None else datetime_lower_limit_value
        for row in revenues_and_datetime:
            revenue = row[0]
            date_time = row[1]
            if(date_time >= datetime_lower_limit_value):
                DatabaseAccessor.update_revenue_historical_data_currrencies(currency, revenue, date_time)


    def __check_time_limit_frame(self, current_date_time, time_limit, time_delta):
        if(time_limit > current_date_time):
            return -1
        elif(time_limit <= current_date_time and time_limit + time_delta > current_date_time):
            return 0
        else:
            return 1

