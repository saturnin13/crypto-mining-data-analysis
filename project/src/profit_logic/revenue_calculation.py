import datetime


class RevenueCalculation():

    @staticmethod
    def calculate_revenue(currency, reward, difficulty, usd_per_currency, revenue_unit=datetime.timedelta(seconds=1), hashrate=1):
        return reward * hashrate / (difficulty * currency.difficulty_one_target()) * revenue_unit.total_seconds() * usd_per_currency