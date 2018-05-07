# crypto-mining-data-analysis
##command line .\project.sh

## PSQL useful
To create a new table:  
CREATE TABLE table_name (LIKE "GRS_historical_data" INCLUDING DEFAULTS INCLUDING CONSTRAINTS INCLUDING INDEXES);  
To rename a column  
ALTER TABLE "XMR_historical_data" RENAME USD_per_GRS TO USD_per_XMR;  
To create a new table live_data:
CREATE TABLE "GTX_1080_TI_live_data"(id serial PRIMARY KEY, ranking INTEGER UNIQUE NOT NULL, currency VARCHAR (255) UNIQUE NOT NULL, profit_per_second DOUBLE PRECISION, profit_per_day DOUBLE PRECISION);

## TO add a new currency historical data fetcher
# Add new table for historical data
create a new table: CREATE TABLE table_name (LIKE "GRS_historical_data" INCLUDING DEFAULTS INCLUDING CONSTRAINTS INCLUDING INDEXES);
rename the column: ALTER TABLE "XMR_historical_data" RENAME USD_per_GRS TO USD_per_XMR;    


# Create a block chain data scrapper
1/ create a class extending GenericBlockchainDataScrapper  
2/ Override the abstract methods  
3/ Add the algorithm to Algorithms class and the currency to Currencies class  
4/ Add the new class to the BlockChainDataScrapperFactory  
  
# Create an exchange rate data scrapper
1/ create a class extending GenericExchangeRateDataScrapper  
2/ Override the abstract methods  
3/ Add the new class to the ExchangeRateDataScrapperFactory  
4/ Add the call to the currency blockchain to CurrenciesDatabaseFilling and adjust time to avoid DDoS protection

# Finally  

1/ Add the call to the currency blockchain to CurrenciesDatabaseFilling and adjust time to avoid DDoS protection
  