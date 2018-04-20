import datetime

import  psycopg2
import psycopg2.extras

from src.currencies.currencies import Currencies


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

        table_name = currency.value.upper() + "_historical_data"
        col_names = ["block_reward", "difficulty", "block_number"]
        col_values = [str(reward), str(difficulty), str(block_number)]

        self.__upsert_time_range(table_name, col_names, col_values, date_time, datetime_lower_limit, datetime_upper_limit)

    def upsert_currency_exchange_rate_historical_data(self, currency, close, date_time, datetime_lower_limit, datetime_upper_limit):
        print("Inserting currency (" + currency.value + "), close exchange rate (" + str(close) + ") and date_time (" + str(date_time) + ")")

        table_name = currency.value.upper() + "_historical_data"
        col_names = [currency.value.upper() + "_per_USD"]
        col_values = [str(close)]

        self.__upsert_time_range(table_name, col_names, col_values, date_time, datetime_lower_limit, datetime_upper_limit)

    def __upsert_time_range(self, table_name, col_names, col_values, date_time, datetime_lower_limit, datetime_upper_limit):
        try:
            self.cur.execute(
                "INSERT INTO \"" + table_name + "\" (" + self.__convert_list_to_string(col_names) + ", datetime) "
                "SELECT " + self.__convert_list_to_string(col_values) + ", '" + str(date_time) + "' "
                    "WHERE NOT EXISTS("
                    "SELECT * "
                    "FROM \"" + table_name + "\" "
                    "WHERE datetime >= '" + str(datetime_lower_limit) + "' AND datetime < '" + str(datetime_upper_limit) + "') "
                "ON CONFLICT DO NOTHING")
            self.cur.execute("UPDATE \"" + table_name + "\" "
                             "SET " + self.__convert_names_values_to_string(col_names, col_values) + " "
                             "WHERE datetime >= '" + str(datetime_lower_limit) + "' AND datetime < '" + str(datetime_upper_limit) + "'")
            self.conn.commit()
        except (psycopg2.DatabaseError) as error:
            print(error)

    def __convert_list_to_string(self, names):
        result = ""
        for i in range(len(names)):
            result += names[i]
            if(i != len(names )- 1):
                result += ", "
        return result

    def __convert_names_values_to_string(self, names, values):
        result = ""
        for i in range(len(names)):
            result += names[i] + "=" + values[i]
            if (i != len(names) - 1):
                result += ", "
        return result


# cur.execute("SELECT * from workers")
# rows = cur.fetchall()
# for row in rows:
#     print ("   " + str(row["id"]))

