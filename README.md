# crypto-mining-data-analysis
##command line .\project.sh

## PSQL useful
to create a new table:
CREATE TABLE table_name (LIKE "GRS_historical_data" INCLUDING DEFAULTS INCLUDING CONSTRAINTS INCLUDING INDEXES);


## TO add a new currency historical data fetcher
# Add new table for historical data
CREATE TABLE table_name (LIKE "GRS_historical_data" INCLUDING DEFAULTS INCLUDING CONSTRAINTS INCLUDING INDEXES);

# Create a block chain data fetcher
1/ create a class extending GenericBlockchainDataScrapper  
2/ Override the abstract methods  
3/ Add the algorithm to Algorithms class and the currency to Currencies class  
4/ Add the new class to the BlockChainDataScrapperFactory  
5/ Add the call to the currency blockchain to CurrenciesDatabaseFilling and adjust time to avoid DDoS protection
  