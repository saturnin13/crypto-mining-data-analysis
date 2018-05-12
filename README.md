# crypto-mining-data-analysis
##command line .\project.sh

## PSQL useful
To create a new table:  
CREATE TABLE table_name (LIKE "GRS_historical_data" INCLUDING DEFAULTS INCLUDING CONSTRAINTS INCLUDING INDEXES);  
To rename a column  
ALTER TABLE "XMR_historical_data" RENAME USD_per_GRS TO USD_per_XMR;  
To create a new table live_data:
CREATE TABLE "GTX_1080_TI_live_data"(id serial PRIMARY KEY, ranking INTEGER UNIQUE NOT NULL, currency VARCHAR (255) UNIQUE NOT NULL, profit_per_second DOUBLE PRECISION, profit_per_day DOUBLE PRECISION);

## To add a new currency historical data fetcher
# Add new table for historical data
create a new table: CREATE TABLE "CURRENCY_historical_data" (LIKE "GRS_historical_data" INCLUDING DEFAULTS INCLUDING CONSTRAINTS INCLUDING INDEXES);
rename the column: ALTER TABLE "CURRENCY_historical_data" RENAME USD_per_GRS TO USD_per_XMR;    


# Create a block chain data scrapper
1/ Find an explorer using coinmarketcap and find api call used by the website most of the time  
2/ create a class extending GenericBlockchainDataScrapper  
3/ Override the abstract methods  
4/ Add the algorithm to Algorithms class and the currency to Currencies class (as well as filling the 3 functions in currency 
(use whatomine and coinmarketwarz to calculate difficultyone target (reward * hashrate / (difficulty * currency.difficulty_one_target()) * revenue_unit.total_seconds() * usd_per_currency)))  
5/ Add the new class to the BlockChainDataScrapperFactory  
  
# Create an exchange rate data scrapper
1/ Find currency on coinmarketcap  
2/ create a class extending GenericExchangeRateDataScrapper  
3/ Override the abstract methods  
4/ Add the new class to the ExchangeRateDataScrapperFactory  

# Finally  

1/ Add the coinmarket api id of the currency in CoinmarketcapDataScrapper (https://api.coinmarketcap.com/v2/listings/)
2/ Adjust time to avoid DDoS protection

  