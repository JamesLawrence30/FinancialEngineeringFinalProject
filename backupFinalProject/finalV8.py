import pandas as pd
from pandas import DataFrame, Series
from datetime import datetime
import datetime as dt
import numpy as np
from numpy import nan
import requests, json, sqlite3, copy


#can only make 5 API calls per minute, and need to make 20, so had to download all the CSV files first
def makeDF(allSymbols, ts_rng):

    date_rng = ts_rng
    df = pd.DataFrame(date_rng, columns=["dateAndTime"])
    	
    for ticker in allSymbols:
    	#only testing with KO and MSFT through wednesday after market close
        csvMACD = './testData/2019_12_02_James2M/__AV01_{}_01.csv'.format(ticker)
        #turn the csv into a data frame with pandas
        dfMACD = pd.DataFrame(pd.read_csv(csvMACD, low_memory=False))

        csvPRICE = './testData/2019_12_02_James1/__AV01_{}_01.csv'.format(ticker)
        dfPRICE = pd.DataFrame(pd.read_csv(csvPRICE, low_memory=False))
        fullImportedData = compareVals(df, dfMACD, dfPRICE, ticker)
        df = combineDFs(df, fullImportedData, ticker)

    return df


def makeTS():
    finalrng=[] #initialize the list that will contain the correct dates and times
    holiday=['2019-11-28']
    #create range with days, wrong times
    days = pd.bdate_range(start='11/25/2019 10:04', end='12/2/2019 16:00', holidays=holiday, freq='C', normalize=False, weekmask='Mon Tue Wed Thu Fri');
    #create our own range using 1 min intervals, but all days of the week
    rng = pd.bdate_range(start='11/25/2019 10:04', end='12/2/2019 16:00', freq='1T', normalize=False);

    #fill list with correct times and days for ts index
    startTime = dt.time(9,31,0);
    endTime = dt.time(16,0,0);
    longdate = rng.date;
    longtime = rng.time;
    shortdate = days.date;
    count=0;
    for day in longdate:
            if day in shortdate:
                    if longtime[count] >= startTime:
                            if longtime[count] <= endTime:
                            		#dont want the seconds since they are't in the imported data to compare with
                                    finalrng.append(rng[count].strftime("%Y-%m-%d %H:%M"))
            count = count+1

    return finalrng[::-1] #prevents inverted range return


#issue is that MACD and price data arent the same range of datetimes..
def compareVals(dfWeBuilt, dfMACD, dfPRICE, symbol):
	#DROP UNNECESSARY COLUMNS:
    dfMACD = dfMACD.drop(['MACD','MACD_Signal'], axis=1) #drop the columns we dont need

    dfPRICE = dfPRICE.drop(['high','low','close','volume'], axis=1) #drop the columns we dont need

    #INSERT ROWS TO MATCH TIMESERIES INDEX
    count=0
    for datetime in dfWeBuilt["dateAndTime"]:
    	#assumes that the datetime start time and end time match rng's start time and end time
    	try:
	        if  str(datetime) != str(dfMACD["time"][count]):
	            dfMACD=insertRow(dfMACD, count, str(datetime)) #add the missing times into the dataframe
	        count=count+1

	    #key error for case where the dataframe's start time is one minute short of rng's start time
    	except KeyError as e:
	        if  str(datetime) != str(dfMACD["time"].iloc[-1]): #comparing to last time in length-1 (last position)
	            dfMACD=endcase(dfMACD, str(datetime)) #add the missing times into the dataframe
	        count=count+1

    counter=0
    for datetime in dfWeBuilt["dateAndTime"]:
        if  str(datetime) != pd.to_datetime(str(dfPRICE["timestamp"][counter])).strftime("%Y-%m-%d %H:%M"):
            dfPRICE=insertRow(dfPRICE, counter, str(datetime)) #add the missing times into the dataframe
        counter=counter+1

    #IF LENGTH OF PRICE AND MACD DONT MATCH, TRIM THE LONGER ONE
    if(dfMACD.shape[0] != dfPRICE.shape[0]):
    	if dfPRICE.shape[0] > dfMACD.shape[0]:
    		for index in [*range(dfPRICE.shape[0])]:
    			if index not in [*range(dfMACD.shape[0])]:
    				dfPRICE.drop(index, inplace=True)
    				#inplace means that the drop applies to this dataframe, doesn't need to be reassigned to a new df
    	else:
    		for index in [*range(dfMACD.shape[0])]:
    			if index not in [*range(dfPRICE.shape[0])]:
    				dfMACD.drop(index)

    return dfMACD, dfPRICE

	
def insertRow(df, rowNum, time):
    # Citation: Used the following as a guide to insert rows into dataframe --
    #https://www.geeksforgeeks.org/insert-row-at-given-position-in-pandas-dataframe/
    dfTop=df[0:rowNum] #first half
    dfBottom=df[rowNum:] #second half
    
    dfTop.loc[rowNum]=[time, np.nan] #add value to the second half
    newDF=pd.concat([dfTop, dfBottom]) #mend the dataframes back together
    newDF.index = [*range(newDF.shape[0])] #need to reaassign the index
    return newDF


def endcase(df, time):
    dfTop=df[0:-2] #first half

    dfBottom=df.iloc[-1] #second half
    
    dfTop.loc[-2]=[time, np.nan] #add value to the second half
    newDF=pd.concat([dfTop, dfBottom]) #mend the dataframes back together
    newDF.index = [*range(newDF.shape[0])] #need to reaassign the index
    return newDF


def combineDFs(dfWeBuilt, dfImported, stock):
    macdDataFrame = dfImported[0]
    priceDataFrame = dfImported[1]

    #add the price of the stock to a column
    priceArray=np.array(priceDataFrame["open"], dtype=np.float) #using open to represent price at the start of the minute
    priceCol="{}_PRICE".format(stock)
    dfWeBuilt[priceCol]=priceArray

    #add the MACD column
    macdCol="{}_MACD".format(stock)
    dfWeBuilt[macdCol]=macdDataFrame["MACD_Hist"]
    
    #put df in chronological order
    dfWeBuilt = dfWeBuilt.iloc[::-1]
	
    #add the gradient of the chronological (reversed) MACD data to a column
    array=np.array(macdDataFrame["MACD_Hist"][::-1], dtype=np.float)
    rateOfChange=np.gradient(array, 1)
    derivCol="{}_GRADIENT".format(stock)
    dfWeBuilt[derivCol]=rateOfChange

    #add the initial signal to a column
    signalList=[]
    allDerivatives = dfWeBuilt[derivCol]
    for deriv in allDerivatives:
    	if deriv > 0:
    		signalList.append("B")
    	elif deriv < 0:
    		signalList.append("S")
    	else:
    		signalList.append("H")
    signalCol="{}_SIGNAL".format(stock)
    dfWeBuilt[signalCol]=signalList

    #create the final trading signal and add to column
    tradeList=[]
    current_signal="H" #hold is default
    allSignals = dfWeBuilt[signalCol]
    for signal in allSignals:
        if signal == "H":
        	tradeList.append("H")
        elif signal == current_signal:
        	tradeList.append("H")
        	current_signal=signal
        else:# signal != current_signal:
        	tradeList.append(signal)
        	current_signal=signal
    tradeCol="{}_TRADE".format(stock)
    dfWeBuilt[tradeCol]=tradeList
    
    #need to reaassign the index
    dfWeBuilt.index = [*range(dfWeBuilt.shape[0])]
    
    #compute profits and percent returns from the trading signals
    profitsTaken=[]
    percentReturns=[]
    currentTradePsn=0
    previousTradePsn=0
    previous_trade="H"
    allTrades = dfWeBuilt[tradeCol]
    
    for trade in allTrades:
        current_price=dfWeBuilt[priceCol][currentTradePsn]
        previous_price=dfWeBuilt[priceCol][previousTradePsn]
        
        #haven't found first trade yet
        if trade == "H" and previous_trade == "H":
        	profitsTaken.append(0)
        	percentReturns.append(0)
        	currentTradePsn=currentTradePsn+1
        	continue
        
        #found first trade, set as first previous trade
        elif previous_trade == "H":
        	if trade == "B":
        		previous_trade = "B"
        	else:# trade == "S":
        		previous_trade = "S"
        
        	profitsTaken.append(0)
        	percentReturns.append(0)
        	previousTradePsn=currentTradePsn
        	currentTradePsn=currentTradePsn+1
        
        elif trade == "S" and previous_trade == "B":
        	long_position=(current_price-previous_price).round(2)
        	profitsTaken.append(long_position) #Long trade
        	long_returns=(((current_price-previous_price)/previous_price)*100).round(2)
        	percentReturns.append(long_returns)
        	previous_trade = "S"
        	previousTradePsn=currentTradePsn
        	currentTradePsn=currentTradePsn+1
        
        elif trade == "B" and previous_trade == "S":
        	short_position=(previous_price-current_price).round(2)
        	profitsTaken.append(short_position) #Short sell
        	short_returns=(((previous_price-current_price)/previous_price)*100).round(2)
        	percentReturns.append(short_returns)
        	previous_trade = "B"
        	previousTradePsn=currentTradePsn
        	currentTradePsn=currentTradePsn+1
        
        else:# trade == "H"
        	profitsTaken.append(0)
        	percentReturns.append(0)
        	currentTradePsn=currentTradePsn+1
        	continue
    		
    profitCol="{}_PROFIT".format(stock)
    dfWeBuilt[profitCol]=profitsTaken

    percentCol="{}_PCT_RTRN".format(stock)
    dfWeBuilt[percentCol]=percentReturns
    
    #put df back in newest to oldest order
    dfWeBuilt = dfWeBuilt.iloc[::-1]

    #need to reaassign the index
    dfWeBuilt.index = [*range(dfWeBuilt.shape[0])]

    return dfWeBuilt


def clean(rawDF):
    #drop row with more than 30% of columns in that row having NaN for that row
    #(many columns have a signal value in the row, so thresh must be low)
    reducedDF = rawDF.dropna(thresh=rawDF.shape[1]*0.7)
    reducedDF.index = [*range(reducedDF.shape[0])] #need to reaassign the index again
    
    #don't fill na with 0 because many values should ACTUALLY be 0 when macd crosses from (-) to (+)
    cleanedDF = reducedDF.fillna(method='ffill')

    #if there were any problems with front filling, fill with 0
    cleanedDF = reducedDF.fillna(0)

    return cleanedDF


def analyze(df, allSymbols):
    #create a list of the total percent returns of each stock over the time period
    all_returns=[]
    for symbol in allSymbols:
        #print(symbol)
        sumReturns=0
        percentCol="{}_PCT_RTRN".format(symbol)
        for percent_return in df[percentCol]:
            if percent_return != 0:
                sumReturns=sumReturns+percent_return
        all_returns.append(sumReturns)
    print("All percent returns:", all_returns)
    avgReturns = np.mean(all_returns).round(2)
    print("Average percent return:", avgReturns)
    varReturns = np.var(all_returns).round(2)
    print("Variance of returns:", varReturns)
    covReturns = np.cov(all_returns).round(2)
    print("Covariance of returns:", covReturns)


def populateDB(df, allSymbols):
    for stock in allSymbols:
        priceCol="{}_PRICE".format(stock)
        macdCol="{}_MACD".format(stock)
        derivCol="{}_GRADIENT".format(stock)
        tradeCol="{}_TRADE".format(stock)
        profitCol="{}_PROFIT".format(stock)
        percentCol="{}_PCT_RTRN".format(stock)


def main():
    allTickers=["MSFT", "KO", "XOM", "INTC", "JNJ", "PG", "PFE", "DIS", "AXP", "GS", "V", "VZ", "WMT", "MCD", "BA", "CSCO", "NKE", "JPM", "MRK", "CVX"]
    rng = makeTS();
    dataframe = makeDF(allTickers, rng); #structure api call by passing in a ticker symbol
    dataframe.to_csv('./hasNullsExport.csv')
    cleanedDF = clean(dataframe)
    cleanedDF.to_csv('./cleanedExport.csv')
    results = analyze(cleanedDF, allTickers)
    #populateDB(cleanedDF, allTickers);#populate database with all time series data


#Tell python to call main function first
if __name__ == "__main__":
    main()
