import  psycopg2
import psycopg2.extras


class DatabaseAccessor:
    def __init__(self):
        try:
            conn = psycopg2.connect(
                "postgres://lncgqbiyoivknm:16497d98c045a638262b080a515986d172cadc0799e23f7ebc1cd225556116a7@ec2-54-217-214-201.eu-west-1.compute.amazonaws.com:5432/dabhdlnlb316fm")
        except:
            print("Unable to connect to the database")
        self.conn = conn
        self.cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    def upsert_currency_blockchain_historical_data(self, currency, reward, difficulty, block_number, date_time, datetime_lower_limit, datetime_upper_limit):
        print("Inserting currency (" + currency.value + "), reward (" + str(reward) + "), difficulty (" + str(difficulty) + ") and date_time (" + str(date_time) + ")")

        table_name = self.__historical_data_table_name(currency)
        col_names = ["block_reward", "difficulty", "block_number"]
        col_values = [str(reward), str(difficulty), str(block_number)]

        self.__upsert_time_range_request(table_name, col_names, col_values, date_time, datetime_lower_limit, datetime_upper_limit)

    def upsert_currency_exchange_rate_historical_data(self, currency, close, date_time, datetime_lower_limit, datetime_upper_limit):
        print("Inserting currency (" + currency.value + "), close exchange rate (" + str(close) + ") and date_time (" + str(date_time) + ")")

        table_name = self.__historical_data_table_name(currency)
        col_names = ["USD_per_" + currency.value.upper()]
        col_values = [str(close)]

        self.__upsert_time_range_request(table_name, col_names, col_values, date_time, datetime_lower_limit, datetime_upper_limit)

    def get_currency_historical_data(self, currency):
        print("Getting currency (" + currency.value + ") historical data")
        return self.__get_data_request(self.__historical_data_table_name(currency))

    def get_graphic_card_data(self, algorithm=None, graphic_card=None):
        print("Getting graphic card data")
        # TODO: put this in helper method which automatically builds the string
        if(algorithm == None and graphic_card == None):
            condition = None
        elif(algorithm == None):
            condition = "algorithm='" + algorithm + "'"
        elif(graphic_card == None):
            condition = "graphic_card='" + graphic_card + "'"
        else:
            condition = "algorithm='" + algorithm + "' AND graphic_card='" + graphic_card + "'"
        return self.__get_data_request("gpu_statistics", condition)

    def update_revenue_historical_data_currrencies(self, currency, revenue, date_time):
        print("Updating currency (" + currency.value + "), with revenue (" + str(revenue) + ") at date_time (" + str(date_time) + ")")
        self.__update_request(self.__historical_data_table_name(currency), ["revenue_per_day_per_hashrate"], [revenue], "datetime='" + str(date_time) + "'")

    def update_cost_gpu_statistics_data(self, algorithm, graphic_card, cost):
        print("Updating algorithm (" + str(algorithm) + ") and graphic_card (" + str(graphic_card) + ") with cost value (" + str(cost) + ")")
        self.__update_request("gpu_statistics", ["cost_per_day_per_hashrate"], [cost], "algorithm='" + str(algorithm) + "' AND graphic_card='" + str(graphic_card) + "'")



    def __get_data_request(self, table_name, conditions=None):
        try:
            conditions = conditions if conditions != None and conditions != "" else "True"
            self.cur.execute("SELECT * "
                             "FROM \"" + table_name + "\" "
                             "WHERE " + conditions)
            return self.cur.fetchall()
        except (psycopg2.DatabaseError) as error:
            raise Exception(error)

    def __upsert_time_range_request(self, table_name, col_names, col_values, date_time, datetime_lower_limit, datetime_upper_limit):
        try:
            self.cur.execute(
                "INSERT INTO \"" + table_name + "\" (" + self.__convert_list_to_string_separated_with_comma(col_names) + ", datetime) "
                "SELECT " + self.__convert_list_to_string_separated_with_comma(col_values) + ", '" + str(date_time) + "' "
                    "WHERE NOT EXISTS("
                    "SELECT * "
                    "FROM \"" + table_name + "\" "
                    "WHERE datetime >= '" + str(datetime_lower_limit) + "' AND datetime < '" + str(datetime_upper_limit) + "') "
                "ON CONFLICT DO NOTHING")
            update_conditions = "datetime >= '" + str(datetime_lower_limit) + "' AND datetime < '" + str(datetime_upper_limit) + "'"
            self.__update_request(table_name, col_names, col_values, update_conditions)
            self.conn.commit()
        except (psycopg2.DatabaseError) as error:
            raise Exception(error)

    def __update_request(self, table_name, col_names, col_values, conditions):
        try:
            self.cur.execute("UPDATE \"" + table_name + "\" "
                             "SET " + self.__convert_names_values_to_string_with_equals(col_names, col_values) + " "
                             "WHERE " + conditions)
            self.conn.commit()
        except (psycopg2.DatabaseError) as error:
            raise Exception(error)

    def __convert_list_to_string_separated_with_comma(self, names):
        result = ""
        for i in range(len(names)):
            if(names[i] == None):
                continue
            result += str(names[i])
            if(i != len(names )- 1):
                result += ", "
        return result

    def __convert_names_values_to_string_with_equals(self, names, values):
        result = ""
        for i in range(len(names)):
            result += str(names[i]) + "=" + str(values[i])
            if (i != len(names) - 1):
                result += ", "
        return result

    def __historical_data_table_name(self, currency):
        return currency.value.upper() + "_historical_data"



