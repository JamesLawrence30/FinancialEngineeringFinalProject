import pandas as pd
from pandas import DataFrame, Series
from datetime import datetime
import datetime as dt
import pandas as pd
import numpy as np
from numpy import nan


#can only make 5 API calls per minute, and need to make 20, so had to download all the CSV files first

def makeDF(symbol):

    date_rng = makeTS();
    df = pd.DataFrame(date_rng, columns=["dateAndTime"])
    print(df)
	
    #for ticker in allSymbols:
    csvLocation = './csvData/technical_indicator_{}.csv'.format(symbol) #go to directory with all the csv files and pick the desired file
    importedDF = pd.DataFrame(pd.read_csv(csvLocation, low_memory=False)) #turn the csv into a data frame with pandas
    fullImportedData = compareVals(df, importedDF)
    print(fullImportedData)
    df = combineDFs(df, fullImportedData, symbol)
    print(df)

    """
    #close loop having added all values from all tickers to the dataframe
    cleanData = clean(df)
    return cleanData
    """


def makeTS():
    finalrng=[] #initialize the list that will contain the correct dates and times
    days = pd.bdate_range(start='11/20/2019 10:04', end='11/26/2019 16:00', freq='C', normalize=False, weekmask='Mon Tue Wed Thu Fri'); #create range with days, wrong times
    rng = pd.bdate_range(start='11/20/2019 10:04', end='11/26/2019 16:00', freq='1T', normalize=False); #create our own range using 1 min intervals, but all days of the week

    #fill list with correct times and days for ts index
    startTime = dt.time(9,30,0);
    endTime = dt.time(16,0,0);
    longdate = rng.date;
    longtime = rng.time;
    shortdate = days.date;
    count=0;
    for day in longdate:
            if day in shortdate:
                    if longtime[count] >= startTime:
                            if longtime[count] <= endTime:
                                    #print(rng[count].strftime("%Y-%m-%d %H:%M"))
                                    finalrng.append(rng[count].strftime("%Y-%m-%d %H:%M")) #dont want the seconds since they are't in the imported data to compare with
            count = count+1

    return finalrng[::-1] #prevents inverted range return


def compareVals(dfWeBuilt, dfImported):
	dfImported = dfImported.drop(['MACD','MACD_Signal'], axis=1) #drop the columns we dont need
	#print(dfImported)
	count=0
	for datetime in dfWeBuilt["dateAndTime"]:
		if  str(datetime) != str(dfImported["time"][count]):
			#print("Missing time:", dfImported["time"][count])
			dfImported=insertRow(dfImported, count, str(datetime)) #add the missing times into the dataframe
		count=count+1

	#print(dfImported)
	return dfImported

	
def insertRow(df, rowNum, time):
	# Citation: Used the following as a guide to insert rows into dataframe -- https://www.geeksforgeeks.org/insert-row-at-given-position-in-pandas-dataframe/
	dfTop=df[0:rowNum] #first half
	dfBottom=df[rowNum:] #second half

	dfTop.loc[rowNum]=[time, np.nan] #add value to the second half
	newDF=pd.concat([dfTop, dfBottom]) #mend the dataframes back together
	newDF.index = [*range(newDF.shape[0])] #need to reaassign the index
	#print(newDF.loc[rowNum])
	return newDF


def combineDFs(dfWeBuilt, dfImported, stock):
	newCol="{}_MACD".format(stock)
	dfWeBuilt[newCol]=dfImported["MACD_Hist"]
	return dfWeBuilt


def clean(rawDF):
    #filledDF = rawDF.fillna(0); #fill blanks with 0
    #filledDF = filledDF.replace({0: np.nan}); #replace all 0 with NaN
    #cleanedDF = filledDF.bfill() #backfill the null values so that no gaps or skews in data exist

    cleanedDF = rawDF.fillna(method=backfill)
    return cleanedDF


def populateDB(df):
    for index, row in df.iterrows():
        #need index, row to access row values by name
        if(float(row["MACD_Signal"]) >= 0.0):
            print("SELL:", row["time"], row["MACD_Signal"]);
        if(float(row["MACD_Signal"]) < 0.0):
            print("BUY:", row["time"], row["MACD_Signal"]);


def main():
    timeSeries = makeDF("MSFT");  #structure api call by passing in a ticker symbol
    #populateDB(timeSeries);#populate database with all time series data
    """
    timeSeries = makeRequest("KO");
    populateDB(timeSeries);
    timeSeries = makeRequest("XOM");
    populateDB(timeSeries);
    timeSeries = makeRequest("INTC");
    populateDB(timeSeries);
    timeSeries = makeRequest("JNJ");
    populateDB(timeSeries);
    timeSeries = makeRequest("PG");
    populateDB(timeSeries);
    timeSeries = makeRequest("DIS");
    populateDB(timeSeries);
    timeSeries = makeRequest("PFE");
    populateDB(timeSeries);
    timeSeries = makeRequest("AXP");
    populateDB(timeSeries);
    timeSeries = makeRequest("GS");
    populateDB(timeSeries);
    timeSeries = makeRequest("V");
    populateDB(timeSeries);
    timeSeries = makeRequest("VZ");
    populateDB(timeSeries);
    timeSeries = makeRequest("WMT");
    populateDB(timeSeries);
    timeSeries = makeRequest("MCD");
    populateDB(timeSeries);
    timeSeries = makeRequest("BA");
    populateDB(timeSeries);
    timeSeries = makeRequest("CSCO");
    populateDB(timeSeries);
    timeSeries = makeRequest("NKE");
    populateDB(timeSeries);
    timeSeries = makeRequest("JPM");
    populateDB(timeSeries);
    timeSeries = makeRequest("MRK");
    populateDB(timeSeries);
    timeSeries = makeRequest("CVX");
    populateDB(timeSeries);
    """


#Tell python to call main function first
if __name__ == "__main__":
    main()
