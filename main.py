# import libraries
# shutil, glob, OS - access files on computer
# smtplib, SSL - send report over email
# get-all-tickers - helps compile list of stocks
import yfinance as yf, pandas as pd
import shutil, os, time, glob, smtplib, ssl


### Extracting stocks of interest 

# List of tickers that we are intested in analyzing
tickers = ["C6L.SI", "D05.SI"] # SIA, DBS
# sia = yf.Ticker(tickers[0])

totalApiCalls = 0
stockFailure = 0
stocksNotImported = 0

##os.mkdir("..\Daily_Stock_Report\Stocks")

for i in tickers:
    
    if (totalApiCalls < 1800): # Max 2000 calls
        
        try:
            stock = i
            tempData = yf.Ticker(stock)
            historicalData = tempData.history(period="max")
            historicalData.to_csv(stock+".csv") 
            time.sleep(2) # pause loop for 2 seconds
            totalApiCalls += 1
            stockFailure = 0
            print(stock + " is loaded")
            
        except ValueError:
            print("Yahoo Finance Backend Error, Attempting to Fix")
             
             # try calling API again for 5 times
            if stockFailure > 5:
                 stocksNotImported +=1
                 
            totalApiCalls += 1
            stockFailure += 1

        else:
            break
             
print("Amount of stocks successfully imported: " + str(len(tickers) - stocksNotImported))
print("Amoount of stocks failed import: " + str(stocksNotImported))
            
## Perform OBV Stock Analysis 

           
