import  psycopg2
import psycopg2.extras


class DatabaseAccessor:
    def __init__(self):
        try:
            conn = psycopg2.connect(
                "postgres://lmxhpacdmmgnfr:0f78fab407cdf1699b50b2fec55a742f65ab1a5cfbbb2c166394a09eb6acf652@ec2-54-247-89-189.eu-west-1.compute.amazonaws.com:5432/denvqvnkc5gm9j")
        except:
            print("Unable to connect to the database")
        self.conn = conn
        self.cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    def upsert_currency_blockchain_historical_data(self, currency, reward, difficulty, block_number, date_time, datetime_lower_limit, datetime_upper_limit):
        print("Inserting currency (" + currency.value + "), reward (" + str(reward) + "), difficulty (" + str(difficulty) + ") and date_time (" + str(date_time) + ")")

        table_name = self.__historical_data_table_name(currency)
        col_names = ["reward", "difficulty", "block_number"]
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
        print("Getting graphic card data for algorithm (" + str(algorithm) +") and graphic card (" + str(graphic_card) + ")")
        # TODO: put this in helper method which automatically builds the string
        if(algorithm == None and graphic_card == None):
            condition = None
        elif(algorithm != None and graphic_card == None):
            condition = "algorithm='" + algorithm + "'"
        elif(graphic_card != None and algorithm == None):
            condition = "graphic_card='" + graphic_card + "'"
        else:
            condition = "algorithm='" + algorithm + "' AND graphic_card='" + graphic_card + "'"
        return self.__get_data_request("gpu_statistics", conditions=condition)

    def update_revenue_historical_data_currrencies(self, currency, revenue, date_time):
        print("Updating currency (" + currency.value + "), with revenue (" + str(revenue) + ") at date_time (" + str(date_time) + ")")
        condition = self.__convert_where_clause(["datetime"], [date_time])
        self.__update_request(self.__historical_data_table_name(currency), ["revenue_per_second_per_hashrate_in_dollar"], [revenue], condition)

    def update_cost_gpu_statistics_data(self, algorithm, graphic_card, cost):
        print("Updating algorithm (" + str(algorithm) + ") and graphic_card (" + str(graphic_card) + ") with cost value (" + str(cost) + ")")
        condition = self.__convert_where_clause(["algorithm", "graphic_card"], [algorithm, graphic_card])
        self.__update_request("gpu_statistics", ["cost_per_second_per_hashrate_per_pricekwh_in_dollar"], [cost], condition)

    def upsert_data_gpu_statistics(self, data):
        print("Upserting gpu_statistics with data: " + str(sorted(data.items())))
        self.__upsert_request("gpu_statistics", list(data.keys()), list(data.values()), conflict_col=["graphic_card", "algorithm", "source"])

    def truncate_table(self, table_name):
        print("Truncating " + str(table_name))
        try:
            self.cur.execute("TRUNCATE TABLE \"" + table_name + "\"")
            self.conn.commit()
        except (psycopg2.DatabaseError) as error:
            raise Exception(error)

    def get_most_recent_valid_row_currency_database(self, currency):
        print("Getting the most recent block number for " + str(currency))
        conditions_string = "block_number IS NOT NULL AND usd_per_" + str(currency) + " IS NOT NULL AND revenue_per_second_per_hashrate_in_dollar IS NOT NULL"
        most_recent_valid_row = self.__get_data_request(str(currency) + "_historical_data", selection="MAX(datetime) as datetime",conditions=conditions_string)[0]["datetime"]

        return self.__get_data_request(str(currency) + "_historical_data", conditions="datetime='" + str(most_recent_valid_row) + "'")[0]

    def update_live_data(self, currency, graphic_card, profit_per_second, profit_per_day, ranking):
        print("Updating live table for " + str(graphic_card) + " and currency " + str(currency) + " with profit " + str(profit_per_second) + " and ranking " + str(ranking))
        self.__upsert_request(str(graphic_card) + "_live_data", ["currency", "profit_per_second", "profit_per_day", "ranking"], [currency, profit_per_second, profit_per_day, ranking], conflict_col=["currency"])

    def create_graphic_card_table(self, graphic_card):
        print("Creating graphic card table for " + str(graphic_card))
        self.__create_table(str(graphic_card) + "_live_data", "id serial PRIMARY KEY, ranking INTEGER UNIQUE NOT NULL, currency VARCHAR (255) UNIQUE NOT NULL, profit_per_second DOUBLE PRECISION, profit_per_day DOUBLE PRECISION")



    def __create_table(self, table_name, col_names):
        try:
            self.cur.execute("CREATE TABLE \"" + table_name + "\"(" + col_names + ")")
            self.conn.commit()
        except (psycopg2.DatabaseError) as error:
            raise Exception(error)

    def __upsert_time_range_request(self, table_name, col_names, col_values, date_time, datetime_lower_limit, datetime_upper_limit):
        exist_condition = "datetime >= '" + str(datetime_lower_limit) + "' AND datetime < '" + str(datetime_upper_limit) + "'"
        col_names.append("datetime")
        col_values.append(date_time)
        self.__upsert_request(table_name, col_names, col_values, exist_condition, conflict_update=False)
        update_conditions = "datetime >= '" + str(datetime_lower_limit) + "' AND datetime < '" + str(datetime_upper_limit) + "'"
        self.__update_request(table_name, col_names, col_values, update_conditions)
        self.conn.commit()

    def __get_data_request(self, table_name, selection="*", conditions=None):
        try:
            conditions = conditions if conditions != None and conditions != "" else "True"
            self.cur.execute("SELECT " + selection + " "
                             "FROM \"" + table_name + "\" "
                             "WHERE " + conditions)
            return self.cur.fetchall()
        except (psycopg2.DatabaseError) as error:
            raise Exception(error)

    def __upsert_request(self, table_name, col_names, col_values, exist_condition="False", conflict_update=True, conflict_col=None):
        try:
            if(conflict_update):
                conflict = "(" + self.__convert_select_clause(conflict_col) + ") DO UPDATE SET " + self.__convert_set_clause(col_names, col_values)
            else:
                conflict = "DO NOTHING"
            self.cur.execute(
                "INSERT INTO \"" + table_name + "\" (" + self.__convert_select_clause(col_names) + ") "
                "SELECT " + self.__convert_select_clause(col_values, apostrophe=True) + " "
                    "WHERE NOT EXISTS("
                    "SELECT * "
                    "FROM \"" + table_name + "\" "
                    "WHERE " + exist_condition + ") "
                "ON CONFLICT " + conflict)
            self.conn.commit()
        except (psycopg2.DatabaseError) as error:
            raise Exception(error)

    def __update_request(self, table_name, col_names, col_values, conditions):
        try:
            self.cur.execute("UPDATE \"" + table_name + "\" "
                             "SET " + self.__convert_set_clause(col_names, col_values) + " "
                             "WHERE " + conditions)
            self.conn.commit()
        except (psycopg2.DatabaseError) as error:
            raise Exception(error)

    def __convert_select_clause(self, names, apostrophe=False):
        return self.__concat_lists(",", names, put_apostrophe=apostrophe)

    def __convert_set_clause(self, names, values):
        return self.__concat_lists(",", names, values=values)

    def __convert_where_clause(self, names, values):
        return self.__concat_lists("AND", names, values=values)

    def __concat_lists(self, separator, names, values=None, put_apostrophe=False):
        result = ""
        apostrophe = ""
        if(put_apostrophe):
            apostrophe = "'"
        for i in range(len(names)):
            current = ""
            if(values is not None):
                if(names[i] is None or values[i] is None):
                    continue
                current = str(names[i]) + "='" + str(values[i]) + "'"
            else:
                if(names[i] is None):
                    continue
                current = str(names[i])
            if (i != 0):
                result += " " + separator + " "
            result += apostrophe + current + apostrophe
        return result

    def __historical_data_table_name(self, currency):
        return currency.value.upper() + "_historical_data"



