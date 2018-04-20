from src.currencies.currencies import Currencies
from src.database_accessor.database_accessor import DatabaseAccessor
import matplotlib.pyplot as plt


db = DatabaseAccessor()
currency_historical_data = db.get_currency_historical_data(Currencies.GRS)
graphic_card_data = db.get_graphic_card_data(Currencies.get_algorithm(Currencies.GRS), "GTX 750 TI")

currency_historical_data.sort(key=lambda x: x["datetime"])

profit_axis = []
date_time_axis = []
day_above_0 = 0
day_under_0 = 0

for row in currency_historical_data[2:]:
    revenue = row["revenue_per_day_per_hashrate"]
    cost = graphic_card_data[0]["cost_per_day_per_hashrate"]
    date_time = row["datetime"]
    if(revenue is None or cost is None or date_time is None):
        continue
    profit = revenue - cost
    if(profit > 0):
        day_above_0 += 1
    else:
        day_under_0 += 1
    profit_axis.append(profit)
    date_time_axis.append(date_time)


print("day_above_0 " + str(day_above_0))
print("day_under_0 " + str(day_under_0))
plt.plot(date_time_axis, profit_axis)
plt.ylabel('some numbers')
plt.axhline(y=0, color='r', linestyle='-')
plt.show()
