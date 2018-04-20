import requests
# url = 'https://rest.coinapi.io/v1/ohlcv/COINEXCHANGE_SPOT_GRS_BTC/history?period_id=1HRS&time_start=2017-01-01T00:00:00'
url = 'https://rest.coinapi.io/v1/ohlcv/COINEXCHANGE_SPOT_GRS_BTC/latest?period_id=5SEC&include_empty_items=true'
# url = 'https://rest.coinapi.io/v1/symbols'
headers = {'X-CoinAPI-Key' : '8F93C8B9-7F38-49D5-AF0A-CA52A1718DC0'}
response = requests.get(url, headers=headers)
# print(response)
# print(response.content)
# print(response.text)