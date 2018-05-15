from contextlib import closing

import  psycopg2
import psycopg2.extras


class DatabaseAccessor:

    @staticmethod
    def upsert_currency_blockchain_historical_data(currency, reward, difficulty, block_number, date_time, datetime_lower_limit, datetime_upper_limit):
        print("Inserting currency (" + currency.value + "), reward (" + str(reward) + "), difficulty (" + str(difficulty) + ") and date_time (" + str(date_time) + ")")

        table_name = DatabaseAccessor.__historical_data_table_name(currency)
        col_names = ["reward", "difficulty", "block_number"]
        col_values = [str(reward), str(difficulty), str(block_number)]

        DatabaseAccessor.__upsert_time_range_request(table_name, col_names, col_values, date_time, datetime_lower_limit, datetime_upper_limit)

    @staticmethod
    def upsert_currency_exchange_rate_historical_data(currency, close, date_time, datetime_lower_limit, datetime_upper_limit):
        print("Inserting currency (" + currency.value + "), close exchange rate (" + str(close) + ") and date_time (" + str(date_time) + ")")

        table_name = DatabaseAccessor.__historical_data_table_name(currency)
        col_names = ["USD_per_" + currency.value.upper()]
        col_values = [str(close)]

        DatabaseAccessor.__upsert_time_range_request(table_name, col_names, col_values, date_time, datetime_lower_limit, datetime_upper_limit)

    @staticmethod
    def get_currency_historical_data(currency):
        print("Getting currency (" + currency.value + ") historical data")
        return DatabaseAccessor.__get_data_request(DatabaseAccessor.__historical_data_table_name(currency))

    @staticmethod
    def get_graphic_card_data(algorithm=None, graphic_card=None):
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
        return DatabaseAccessor.__get_data_request("gpu_statistics", conditions=condition)

    @staticmethod
    def update_revenue_historical_data_currrencies(currency, revenue, date_time):
        print("Updating currency (" + currency.value + "), with revenue (" + str(revenue) + ") at date_time (" + str(date_time) + ")")
        condition = DatabaseAccessor.__convert_where_clause(["datetime"], [date_time])
        DatabaseAccessor.__update_request(DatabaseAccessor.__historical_data_table_name(currency), ["revenue_per_second_per_hashrate_in_dollar"], [revenue], condition)

    @staticmethod
    def update_cost_gpu_statistics_data(algorithm, graphic_card, cost):
        print("Updating algorithm (" + str(algorithm) + ") and graphic_card (" + str(graphic_card) + ") with cost value (" + str(cost) + ")")
        condition = DatabaseAccessor.__convert_where_clause(["algorithm", "graphic_card"], [algorithm, graphic_card])
        DatabaseAccessor.__update_request("gpu_statistics", ["cost_per_second_per_hashrate_per_pricekwh_in_dollar"], [cost], condition)

    @staticmethod
    def upsert_data_gpu_statistics(data):
        print("Upserting gpu_statistics with data: " + str(sorted(data.items())))
        DatabaseAccessor.__upsert_request("gpu_statistics", list(data.keys()), list(data.values()), conflict_col=["graphic_card", "algorithm", "source"])

    @staticmethod
    def truncate_table(table_name):
        print("Truncating " + str(table_name))
        with closing(DatabaseAccessor.__get_connection()) as conn:
            with conn, conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as curr:
                curr.execute("TRUNCATE TABLE \"" + table_name + "\"")
                conn.commit()

    @staticmethod
    def get_most_recent_valid_row_currency_database(currency):
        print("Getting the most recent block number for " + str(currency))
        conditions_string = "block_number IS NOT NULL AND usd_per_" + str(currency) + " IS NOT NULL AND revenue_per_second_per_hashrate_in_dollar IS NOT NULL"
        most_recent_valid_row = DatabaseAccessor.__get_data_request(str(currency) + "_historical_data", selection="MAX(datetime) as datetime",conditions=conditions_string)[0]["datetime"]
        if(not most_recent_valid_row):
            return None
        return DatabaseAccessor.__get_data_request(str(currency) + "_historical_data", conditions="datetime='" + str(most_recent_valid_row) + "'")[0]

    @staticmethod
    def update_live_data(currency, graphic_card, profit_per_second, profit_per_day, ranking):
        print("Updating live table for " + str(graphic_card) + " and currency " + str(currency) + " with profit " + str(profit_per_second) + " and ranking " + str(ranking))
        DatabaseAccessor.__upsert_request(str(graphic_card) + "_live_data", ["currency", "profit_per_second", "profit_per_day", "ranking"],
                                          [currency, profit_per_second, profit_per_day, ranking], conflict_col=["currency"])
    @staticmethod
    def create_graphic_card_table(graphic_card):
        print("Creating graphic card table for " + str(graphic_card))
        DatabaseAccessor.__create_table(str(graphic_card) + "_live_data", "id serial PRIMARY KEY, ranking INTEGER UNIQUE NOT NULL, currency VARCHAR (255) UNIQUE NOT NULL, profit_per_second DOUBLE PRECISION, profit_per_day DOUBLE PRECISION")

    @staticmethod
    def update_release_date_gpu_statistics_data(graphic_card, release_date):
        print("Updating graphic_card (" + str(graphic_card) + ") with release date (" + str(release_date) + ")")
        DatabaseAccessor.__update_request("gpu_statistics", ["release_date"], [release_date], DatabaseAccessor.__convert_where_clause(["graphic_card"], [str(graphic_card)]))

    @staticmethod
    def create_historical_data_table_currency(currency):
        print("Create historical data table for currency " + str(currency))
        DatabaseAccessor.__create_table(str(currency) + "_historical_data", "LIKE \"GRS_historical_data\" INCLUDING DEFAULTS INCLUDING CONSTRAINTS INCLUDING INDEXES")
        try:
            DatabaseAccessor.__alter_table(str(currency) + "_historical_data", "USD_per_GRS", "USD_per_" + str(currency))
        except psycopg2.ProgrammingError as error:
            if(str(error) != "column \"usd_per_grs\" does not exist\n" and str(error) != "column \"usd_per_grs\" of relation \"GRS_historical_data\" already exists\n"):
                raise error


    @staticmethod
    def __alter_table(table_name, replaced_col, replacing_col):
        with closing(DatabaseAccessor.__get_connection()) as conn:
            with conn, conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as curr:
                curr.execute("ALTER TABLE \"" + table_name + "\" RENAME " + replaced_col + " TO " + replacing_col)
                conn.commit()

    @staticmethod
    def __create_table(table_name, col_names):
        with closing(DatabaseAccessor.__get_connection()) as conn:
            with conn, conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as curr:
                curr.execute("CREATE TABLE IF NOT EXISTS \"" + table_name + "\"(" + col_names + ")")
                conn.commit()

    @staticmethod
    def __get_data_request(table_name, selection="*", conditions=None):
        with closing(DatabaseAccessor.__get_connection()) as conn:
            with conn, conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as curr:
                conditions = conditions if conditions != None and conditions != "" else "True"
                curr.execute("SELECT " + selection + " "
                                 "FROM \"" + table_name + "\" "
                                 "WHERE " + conditions)
                result = curr.fetchall()

                return result

    @staticmethod
    def __upsert_time_range_request(table_name, col_names, col_values, date_time, datetime_lower_limit, datetime_upper_limit):
        exist_condition = "datetime >= '" + str(datetime_lower_limit) + "' AND datetime < '" + str(datetime_upper_limit) + "'"
        col_names.append("datetime")
        col_values.append(date_time)
        DatabaseAccessor.__upsert_request(table_name, col_names, col_values, exist_condition, conflict_update=False)
        update_conditions = "datetime >= '" + str(datetime_lower_limit) + "' AND datetime < '" + str(datetime_upper_limit) + "'"
        DatabaseAccessor.__update_request(table_name, col_names, col_values, update_conditions)

    @staticmethod
    def __upsert_request(table_name, col_names, col_values, exist_condition="False", conflict_update=True, conflict_col=None):
        with closing(DatabaseAccessor.__get_connection()) as conn:
            with conn, conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as curr:
                if(conflict_update):
                    conflict = "(" + DatabaseAccessor.__convert_select_clause(conflict_col) + ") DO UPDATE SET " + DatabaseAccessor.__convert_set_clause(col_names, col_values)
                else:
                    conflict = "DO NOTHING"
                curr.execute(
                "INSERT INTO \"" + table_name + "\" (" + DatabaseAccessor.__convert_select_clause(col_names) + ") "
                "SELECT " + DatabaseAccessor.__convert_select_clause(col_values, apostrophe=True) + " "
                    "WHERE NOT EXISTS("
                    "SELECT * "
                    "FROM \"" + table_name + "\" "
                    "WHERE " + exist_condition + ") "
                "ON CONFLICT " + conflict)
                conn.commit()

    @staticmethod
    def __update_request(table_name, col_names, col_values, conditions):
        with closing(DatabaseAccessor.__get_connection()) as conn:
            with conn, conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as curr:
                curr.execute("UPDATE \"" + table_name + "\" "
                                 "SET " + DatabaseAccessor.__convert_set_clause(col_names, col_values) + " "
                                 "WHERE " + conditions)
                conn.commit()

    @staticmethod
    def __convert_set_clause(names, values):
        return DatabaseAccessor.__concat_lists(",", names, values=values)

    @staticmethod
    def __convert_select_clause(names, apostrophe=False):
        return DatabaseAccessor.__concat_lists(",", names, put_apostrophe=apostrophe)

    @staticmethod
    def __convert_where_clause(names, values):
        return DatabaseAccessor.__concat_lists("AND", names, values=values)

    @staticmethod
    def __concat_lists(separator, names, values=None, put_apostrophe=False):
        result = ""
        apostrophe = ""
        if(put_apostrophe):
            apostrophe = "'"
        for i in range(len(names)):
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


    @staticmethod
    def __get_connection():
        try:
            return psycopg2.connect("postgres://lmxhpacdmmgnfr:0f78fab407cdf1699b50b2fec55a742f65ab1a5cfbbb2c166394a09eb6acf652@ec2-54-247-89-189.eu-west-1.compute.amazonaws.com:5432/denvqvnkc5gm9j")
        except:
            raise Exception("Unable to connect to the database")

    @staticmethod
    def __historical_data_table_name(currency):
        return currency.value.upper() + "_historical_data"

