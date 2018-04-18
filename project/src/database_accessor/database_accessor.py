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

    def upsert_currency_historical_data(self, currency, reward, difficulty, block_number, date_time, datetime_lower_limit, datetime_upper_limit):
        print("Inserting curency (" + currency.value + "), reward (" + str(reward) + "), difficulty (" + str(difficulty) + ") and date_time (" + str(date_time) + ")")
        try:
            self.cur.execute("INSERT INTO \"" + currency.value.upper() + "_historical_data\" (block_reward, difficulty, block_number, datetime) "
                             "SELECT " + str(reward) + ", " + str(difficulty) + ", " + str(block_number) + ", '" + str(date_time) + "' "
                             "WHERE NOT EXISTS("
                                "SELECT * "
                                "FROM \"" + currency.value.upper() + "_historical_data\" "
                                "WHERE datetime > '" + str(datetime_lower_limit) + "' AND datetime < '" + str(datetime_upper_limit) + "') "
                              "ON CONFLICT DO NOTHING")
            self.conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)


# cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
# cur.execute("SELECT * from workers")
# rows = cur.fetchall()
# print("\nShow me the databases:\n")
# for row in rows:
#     print ("   " + str(row["id"]))



