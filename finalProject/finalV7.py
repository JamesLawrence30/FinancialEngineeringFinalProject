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
    #print("range:", df)
    	
    for ticker in allSymbols:
        csvMACD = './testData/2019_12_02_James2M/__AV01_{}_01.csv'.format(ticker) #only testing with KO and MSFT through wednesday after market close
        dfMACD = pd.DataFrame(pd.read_csv(csvMACD, low_memory=False)) #turn the csv into a data frame with pandas

        #***may need to delete the csv rows with timestamps that don't line up with MACD times***
        csvPRICE = './testData/2019_12_02_James1/__AV01_{}_01.csv'.format(ticker) #only testing with KO and MSFT through wednesday after market close
        dfPRICE = pd.DataFrame(pd.read_csv(csvPRICE, low_memory=False)) #turn the csv into a data frame with pandas	
        fullImportedData = compareVals(df, dfMACD, dfPRICE, ticker)
        #print(fullImportedData[0])
        #print(fullImportedData[1])
        df = combineDFs(df, fullImportedData, ticker)
        #print(df)
    return df


def makeTS():
    finalrng=[] #initialize the list that will contain the correct dates and times
    holiday=['2019-11-28']
    days = pd.bdate_range(start='11/25/2019 10:04', end='12/2/2019 16:00', holidays=holiday, freq='C', normalize=False, weekmask='Mon Tue Wed Thu Fri'); #create range with days, wrong times
    rng = pd.bdate_range(start='11/25/2019 10:04', end='12/2/2019 16:00', freq='1T', normalize=False); #create our own range using 1 min intervals, but all days of the week

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
                                    #print(rng[count].strftime("%Y-%m-%d %H:%M"))
                                    finalrng.append(rng[count].strftime("%Y-%m-%d %H:%M")) #dont want the seconds since they are't in the imported data to compare with
            count = count+1

    return finalrng[::-1] #prevents inverted range return

#issue is that MACD and price data arent the same range of datetimes..
def compareVals(dfWeBuilt, dfMACD, dfPRICE, symbol):
	#DROP UNNECESSARY COLUMNS:
    dfMACD = dfMACD.drop(['MACD','MACD_Signal'], axis=1) #drop the columns we dont need
    #print(symbol, "MACD start:")######################################################################
    #print(dfMACD)######################################################################

    dfPRICE = dfPRICE.drop(['high','low','close','volume'], axis=1) #drop the columns we dont need
    #print(symbol, "Price start:")######################################################################
    #print(dfPRICE)######################################################################

    #INSERT ROWS TO MATCH TIMESERIES INDEX
    count=0
    for datetime in dfWeBuilt["dateAndTime"]:
    	#assumes that the datetime start time and end time match rng's start time and end time
    	try:
	        if  str(datetime) != str(dfMACD["time"][count]):
	            #print("Missing time:", dfMACD["time"][count])
	            dfMACD=insertRow(dfMACD, count, str(datetime)) #add the missing times into the dataframe
	            #print(dfMACD) ########
	        count=count+1

	    #key error for case where the dataframe's start time is one minute short of rng's start time
    	except KeyError as e:
	        #print(e)
	        if  str(datetime) != str(dfMACD["time"].iloc[-1]): #comparing to last time in length-1 (last position)
	            dfMACD=endcase(dfMACD, str(datetime)) #add the missing times into the dataframe
	        count=count+1

    #print("MACD done:")
    #print(dfMACD)

    counter=0
    for datetime in dfWeBuilt["dateAndTime"]:
        if  str(datetime) != pd.to_datetime(str(dfPRICE["timestamp"][counter])).strftime("%Y-%m-%d %H:%M"):
            #print(str(datetime), pd.to_datetime(str(dfPRICE["timestamp"][counter])).strftime("%Y-%m-%d %H:%M")) ########
            #print("Missing time:", dfPRICE["timestamp"][counter])
            dfPRICE=insertRow(dfPRICE, counter, str(datetime)) #add the missing times into the dataframe
        counter=counter+1
    #print("Price done:")
    #print(dfPRICE)

    #IF LENGTH OF PRICE AND MACD DONT MATCH, TRIM THE LONGER ONE
    if(dfMACD.shape[0] != dfPRICE.shape[0]):
    	if dfPRICE.shape[0] > dfMACD.shape[0]:
    		for index in [*range(dfPRICE.shape[0])]:
    			if index not in [*range(dfMACD.shape[0])]:
    				#print(index)
    				dfPRICE.drop(index, inplace=True) #inplace means that the drop applies to this dataframe, doesn't need to be reassigned to a new df
    	else:
    		for index in [*range(dfMACD.shape[0])]:
    			if index not in [*range(dfPRICE.shape[0])]:
    				dfMACD.drop(index)

    #print(symbol, "MACD done:")######################################################################
    #print(dfMACD)######################################################################
    #print(symbol, "Price done:")######################################################################
    #print(dfPRICE)######################################################################
    return dfMACD, dfPRICE

	
def insertRow(df, rowNum, time):
    # Citation: Used the following as a guide to insert rows into dataframe -- https://www.geeksforgeeks.org/insert-row-at-given-position-in-pandas-dataframe/
    dfTop=df[0:rowNum] #first half
    #print(dfTop)
    dfBottom=df[rowNum:] #second half
    #print(dfBottom)
    
    dfTop.loc[rowNum]=[time, np.nan] #add value to the second half
    newDF=pd.concat([dfTop, dfBottom]) #mend the dataframes back together
    newDF.index = [*range(newDF.shape[0])] #need to reaassign the index
    #print(newDF.loc[rowNum])
    return newDF


def endcase(df, time):
    dfTop=df[0:-2] #first half
    #print(dfTop)

    dfBottom=df.iloc[-1] #second half
    #print(dfBottom)
    
    dfTop.loc[-2]=[time, np.nan] #add value to the second half
    newDF=pd.concat([dfTop, dfBottom]) #mend the dataframes back together
    newDF.index = [*range(newDF.shape[0])] #need to reaassign the index
    return newDF

def combineDFs(dfWeBuilt, dfImported, stock):
    macdDataFrame = dfImported[0]
    priceDataFrame = dfImported[1]
	
    #add the MACD column
    macdCol="{}_MACD".format(stock)
    dfWeBuilt[macdCol]=macdDataFrame["MACD_Hist"]
	
    #add the gradient of the MACD to a column
    array=np.array(macdDataFrame["MACD_Hist"], dtype=np.float)
    rateOfChange=np.gradient(array)
    derivCol="{}_GRADIENT".format(stock)
    dfWeBuilt[derivCol]=rateOfChange

    #add the price of the stock to a column
    priceArray=np.array(priceDataFrame["open"], dtype=np.float) #using open to represent price at the start of the minute
    priceCol="{}_PRICE".format(stock)
    dfWeBuilt[priceCol]=priceArray

    return dfWeBuilt


def clean(rawDF):
    #drop row with more than 50% of columns in that row having NaN for that row
    reducedDF = rawDF.dropna(thresh=rawDF.shape[1]*0.5)
    
    #don't fill na with 0 because many values should ACTUALLY be 0 when macd crosses from (-) to (+)
    cleanedDF = reducedDF.fillna(method='ffill')
    return cleanedDF


def populateDB(df):
	dateAndTime = df["dateAndTime"]
    #
    MSFT_MACD = df["MSFT_MACD"]
    MSFT_GRADIENT = df["MSFT_GRADIENT"]
    MFST_PRICE = df["MFST_PRICE"]
    MFST_TRADE = df["MFST_TRADE"]
    MFST_PROFIT = df["MFST_PROFIT"]
    MFST_%_RETURN = df["MFST_%_RETURN"]
    #
    KO_MACD = df["KO_MACD"] 
    KO_GRADIENT = df["KO_GRADIENT"]
    KO_PRICE = df["KO_PRICE"]
    KO_TRADE = df["KO_TRADE"]
    KO_PROFIT = df["KO_PROFIT"]
    KO_%_RETURN = df["KO_%_RETURN"]
    #
    XOM_MACD = df["XOM_MACD"]
    XOM_GRADIENT = df["XOM_GRADIENT"]
    XOM_PRICE = df["XOM_PRICE"]
    XOM_TRADE = df["XOM_TRADE"]
    XOM_PROFIT = df["XOM_PROFIT"]
    XOM_%_RETURN = df["XOM_%_RETURN"]
    #
    INTC_MACD = df["INTC_MACD"]
    INTC_GRADIENT = df["INTC_GRADIENT"]
    INTC_PRICE = df["INTC_PRICE"]
    INTC_TRADE = df["INTC_TRADE"]
    INTC_PROFIT = df["INTC_PROFIT"]
    INTC_%_RETURN = df["INTC_%_RETURN"]
    #
    JNJ_MACD = df["JNJ_MACD"]
    JNJ_GRADIENT = df["JNJ_GRADIENT"]
    JNJ_PRICE = df["JNJ_PRICE"]
    JNJ_TRADE = df["JNJ_TRADE"]
    JNJ_PROFIT = df["JNJ_PROFIT"]
    JNJ_%_RETURN = df["JNJ_%_RETURN"]
    #
    PG_MACD = df["PG_MACD"]
    PG_GRADIENT = df["PG_GRADIENT"]
    PG_PRICE = df["PG_PRICE"]
    PG_TRADE = df["PG_TRADE"]
    PG_PROFIT = df["PG_PROFIT"]
    PG_%_RETURN = df["PG_%_RETURN"]
    #
    PFE_MACD = df["PFE_MACD"]
    PFE_GRADIENT = df["PFE_GRADIENT"]
    PFE_PRICE = df["PFE_PRICE"]
    PFE_TRADE = df["PFE_TRADE"]
    PFE_PROFIT = df["PFE_PROFIT"]
    PFE_%_RETURN = df["PFE_RETURN"]
    #
    DIS_MACD = df["DIS_MACD"]
    DIS_GRADIENT = df["DIS_GRADIENT"]
    DIS_PRICE = df["DIS_PRICE"]
    DIS_TRADE = df["DIS_TRADE"]
    DIS_PROFIT = df["DIS_PROFIT"]
    DIS_%_RETURN = df["DIS_%_RETURN"]
    #
    AXP_MACD = df["AXP_MACD"]
    AXP_GRADIENT = df["AXP_GRADIENT"]
    AXP_PRICE = df["AXP_PRICE"]
    AXP_TRADE = df["AXP_TRADE"]
    AXP_PROFIT = df["AXP_PROFIT"]
    AXP_%_RETURN = df["AXP_%_RETURN"]
    #
    GS_MACD = df["GS_MACD"]
    GS_GRADIENT = df["GS_GRADIENT"]
    GS_PRICE = df["GS_PRICE"]
    GS_TRADE = df["GS_TRADE"]
    GS_PROFIT = df["GS_PROFIT"]
    GS_%_RETURN = df["GS_%_RETURN"]
    #
    V_MACD = df["V_MACD"]
    V_GRADIENT = df["V_GRADIENT"]
    V_PRICE = df["V_PRICE"]
    V_TRADE = df["V_TRADE"]
    V_PROFIT = df["V_PROFIT"]
    V_%_RETURN = df["V_%_RETURN"]
    #
    VZ_MACD = df["VZ_MACD"]
    VZ_GRADIENT = df["VZ_GRADIENT"]
    VZ_PRICE = df["VZ_PRICE"]
    VZ_TRADE = df["VZ_TRADE"]
    VZ_PROFIT = df["VZ_PROFIT"]
    VZ_%_RETURN = df["VZ_%_RETURN"]
    #
    WMT_MACD = df["WMT_MACD"]
    WMT_GRADIENT = df["WMT_GRADIENT"]
    WMT_PRICE = df["WMT_PRICE"]
    WMT_TRADE = df["WMT_TRADE"]
    WMT_PROFIT = df["WMT_PROFIT"]
    WMT_%_RETURN = df["WMT_%_RETURN"]
    #
    MCD_MACD = df["MCD_MACD"]
    MCD_GRADIENT = df["MCD_GRADIENT"]
    MCD_PRICE = df["MCD_PRICE"]
    MCD_TRADE = df["MCD_TRADE"]
    MCD_PROFIT = df["MCD_PROFIT"]
    MCD_%_RETURN = df["MCD_%_RETURN"]
    #
    BA_MACD = df["BA_MACD"]
    BA_GRADIENT = df["BA_GRADIENT"]
    BA_PRICE = df["BA_PRICE"]
    BA_TRADE = df["BA_TRADE"]
    BA_PROFIT = df["BA_PROFIT"]
    BA_%_RETURN = df["BA_%_RETURN"]
    #
    CSCO_MACD = df["CSCO_MACD"]
    CSCO_GRADIENT = df["CSCO_GRADIENT"]
    CSCO_PRICE = df["CSCO_PRICE"]
    CSCO_TRADE = df["CSCO_TRADE"]
    CSCO_PROFIT = df["CSCO_PROFIT"]
    CSCO_%_RETURN = df["CSCO_%_RETURN"]
    #
    NKE_MACD = df["NKE_MACD"]
    NKE_GRADIENT = df["NKE_GRADIENT"]
    NKE_PRICE = df["NKE_PRICE"]
    NKE_TRADE = df["NKE_TRADE"]
    NKE_PROFIT = df["NKE_PROFIT"]
    NKE_%_RETURN = df["NKE_%_RETURN"]
    #
    JPM_MACD = df["JPM_MACD"]
    JPM_GRADIENT = df["JPM_GRADIENT"]
    JPM_PRICE = df["JPM_PRICE"]
    JPM_TRADE = df["MFST_TRADE"]
    JPM_PROFIT = df["JPM_PROFIT"]
    JPM_%_RETURN = df["JPM_%_RETURN"]
    #
    MRK_MACD = df["MRK_MACD"]
    MRK_GRADIENT = df["MRK_GRADIENT"]
    MRK_PRICE = df["MRK_PRICE"]
    MRK_TRADE = df["MRK_TRADE"]
    MRK_PROFIT = df["MRK_PROFIT"]
    MRK_%_RETURN = df["MRK_%_RETURN"]
    #
    CVX_MACD = df["CVX_MACD"]
    CVX_GRADIENT = df["CVX_GRADIENT"]
    CVX_PRICE = df["CVX_PRICE"]
    CVX_TRADE = df["CVX_TRADE"]
    CVX_PROFIT = df["CVX_PROFIT"]
    CVX_%_RETURN = df["CVX_%_RETURN"]
    
    for index, row in df.iterrows():
        #need index, row to access row values by name
        if(float(row["MACD_Signal"]) >= 0.0):
            print("SELL:", row["time"], row["MACD_Signal"]);
        if(float(row["MACD_Signal"]) < 0.0):
            print("BUY:", row["time"], row["MACD_Signal"]);




def main():
    allTickers=["MSFT", "KO", "XOM", "INTC", "JNJ", "PG", "PFE", "DIS", "AXP", "GS", "V", "VZ", "WMT", "MCD", "BA", "CSCO", "NKE", "JPM", "MRK", "CVX"]
    #testing with only MSFT and KO for now..will add all MACD and price data for other stocks on Wednesday night
    #allTickers=["MSFT", "KO"]
    rng = makeTS();
    dataframe = makeDF(allTickers, rng);  #structure api call by passing in a ticker symbol
    dataframe.to_csv('./hasNullsExport.csv')
    cleanedDF = clean(dataframe)
    cleanedDF.to_csv('./cleanedExport.csv')
    populateDB(cleanedDF);#populate database with all time series data


#Tell python to call main function first
if __name__ == "__main__":
    main()
