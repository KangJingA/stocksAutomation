# import libraries
# shutil, glob, OS - access files on computer
# smtplib, SSL - send report over email

import yfinance as yf, pandas as pd
import shutil, os, time, glob, smtplib, ssl

### Extracting stocks of interest 

# List of tickers that we are intested in analyzing
tickers = ["C6L.SI", "D05.SI"] # SIA, DBS
# sia = yf.Ticker(tickers[0])

totalApiCalls = 0
stockFailure = 0
stocksNotImported = 0


if os.path.exists("dailyStockReport\\stocks"):
    shutil.rmtree("dailyStockReport\\stocks")


os.mkdir("dailyStockReport\\stocks")

for i in tickers:
    
    if (totalApiCalls < 1800): # Max 2000 calls
        
        try:
            stock = i
            tempData = yf.Ticker(stock)
            historicalData = tempData.history(period="max")
            historicalData.to_csv("dailyStockReport\\stocks\\" +stock+".csv") 
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

             
print("Amount of stocks successfully imported: " + str(len(tickers) - stocksNotImported))
print("Amoount of stocks failed import: " + str(stocksNotImported))
            
## Perform OBV Stock Analysis from extracted data

# grab list of file paths
list_files = (glob.glob("dailyStockReport\\stocks\\*.csv"))
OBV_data = []
tradingDays = 10 # number of trading days to observe

for file in list_files:

    # read each file and grab the data from the last 10 days
    stockData = pd.read_csv(file).tail(tradingDays)
    positiveMove, negativeMove = [], []

    for i in range(tradingDays):
        
        if stockData.iloc[i,1] < stockData.iloc[i,4]: # open vs close
           positiveMove.append(i) #grab the days

        elif stockData.iloc[i,1] > stockData.iloc[i,4]:
            negativeMove.append(i)
        
    # update OBV value
    OBV_value_pos = [stockData.iloc[i,5]/stockData.iloc[i,1] for i in positiveMove]
    OBV_value_neg = [stockData.iloc[i,5]/stockData.iloc[i,1] for i in negativeMove]
    OBV_value = sum(OBV_value_pos) - sum(OBV_value_neg)
    Stock_Name = ((os.path.basename(file)).split(".csv")[0])  # Get the name of the current stock we are analyzing
    OBV_data.append([Stock_Name, OBV_value])  # Add the stock name and OBV value to the new_data list

final_df = pd.DataFrame(OBV_data, columns = ["Ticker", "OBV Value"])

final_df["Stocks_Ranked"] = final_df["OBV Value"].rank(ascending = False)  # Rank the stocks by their OBV_Values
final_df.sort_values("OBV Value", inplace = True, ascending = False)  # Sort the ranked stocks
final_df.to_csv("dailyStockReport\\OBV_Ranked.csv", index = False)  # Save the dataframe to a csv without the index column