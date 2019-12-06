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
    #drop row with more than 30% of columns in that row having NaN for that row (many columns have a signal value in the row, so thresh must be low)
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
    dateAndTime = df["dateAndTime"]
    MSFT_MACD = df["MSFT_MACD"]
    MSFT_GRADIENT = df["MSFT_GRADIENT"]
    MSFT_PRICE = df["MSFT_PRICE"]
    MSFT_TRADE = df["MSFT_TRADE"]
    MSFT_PROFIT = df["MSFT_PROFIT"]
    MSFT_RETURN = df["MSFT_RETURN"]
    #
    KO_MACD = df["KO_MACD"]
    KO_GRADIENT = df["KO_GRADIENT"]
    KO_PRICE = df["KO_PRICE"]
    KO_TRADE = df["KO_TRADE"]
    KO_PROFIT = df["KO_PROFIT"]
    KO_RETURN = df["KO_RETURN"]
    #
    XOM_MACD = df["XOM_MACD"]
    XOM_GRADIENT = df["XOM_GRADIENT"]
    XOM_PRICE = df["XOM_PRICE"]
    XOM_TRADE = df["XOM_TRADE"]
    XOM_PROFIT = df["XOM_PROFIT"]
    XOM_RETURN = df["XOM_RETURN"]
    #
    INTC_MACD = df["INTC_MACD"]
    INTC_GRADIENT = df["INTC_GRADIENT"]
    INTC_PRICE = df["INTC_PRICE"]
    INTC_TRADE = df["INTC_TRADE"]
    INTC_PROFIT = df["INTC_PROFIT"]
    INTC_RETURN = df["INTC_RETURN"]
    #
    JNJ_MACD = df["JNJ_MACD"]
    JNJ_GRADIENT = df["JNJ_GRADIENT"]
    JNJ_PRICE = df["JNJ_PRICE"]
    JNJ_TRADE = df["JNJ_TRADE"]
    JNJ_PROFIT = df["JNJ_PROFIT"]
    JNJ_RETURN = df["JNJ_RETURN"]
    #
    PG_MACD = df["PG_MACD"]
    PG_GRADIENT = df["PG_GRADIENT"]
    PG_PRICE = df["PG_PRICE"]
    PG_TRADE = df["PG_TRADE"]
    PG_PROFIT = df["PG_PROFIT"]
    PG_RETURN = df["PG_RETURN"]
    #
    PFE_MACD = df["PFE_MACD"]
    PFE_GRADIENT = df["PFE_GRADIENT"]
    PFE_PRICE = df["PFE_PRICE"]
    PFE_TRADE = df["PFE_TRADE"]
    PFE_PROFIT = df["PFE_PROFIT"]
    PFE_RETURN = df["PFE_RETURN"]
    #
    DIS_MACD = df["DIS_MACD"]
    DIS_GRADIENT = df["DIS_GRADIENT"]
    DIS_PRICE = df["DIS_PRICE"]
    DIS_TRADE = df["DIS_TRADE"]
    DIS_PROFIT = df["DIS_PROFIT"]
    DIS_RETURN = df["DIS_RETURN"]
    #
    AXP_MACD = df["AXP_MACD"]
    AXP_GRADIENT = df["AXP_GRADIENT"]
    AXP_PRICE = df["AXP_PRICE"]
    AXP_TRADE = df["AXP_TRADE"]
    AXP_PROFIT = df["AXP_PROFIT"]
    AXP_RETURN = df["AXP_RETURN"]
    #
    GS_MACD = df["GS_MACD"]
    GS_GRADIENT = df["GS_GRADIENT"]
    GS_PRICE = df["GS_PRICE"]
    GS_TRADE = df["GS_TRADE"]
    GS_PROFIT = df["GS_PROFIT"]
    GS_RETURN = df["GS_RETURN"]
    #
    V_MACD = df["V_MACD"]
    V_GRADIENT = df["V_GRADIENT"]
    V_PRICE = df["V_PRICE"]
    V_TRADE = df["V_TRADE"]
    V_PROFIT = df["V_PROFIT"]
    V_RETURN = df["V_RETURN"]
    #
    VZ_MACD = df["VZ_MACD"]
    VZ_GRADIENT = df["VZ_GRADIENT"]
    VZ_PRICE = df["VZ_PRICE"]
    VZ_TRADE = df["VZ_TRADE"]
    VZ_PROFIT = df["VZ_PROFIT"]
    VZ_RETURN = df["VZ_RETURN"]
    #
    WMT_MACD = df["WMT_MACD"]
    WMT_GRADIENT = df["WMT_GRADIENT"]
    WMT_PRICE = df["WMT_PRICE"]
    WMT_TRADE = df["WMT_TRADE"]
    WMT_PROFIT = df["WMT_PROFIT"]
    WMT_RETURN = df["WMT_RETURN"]
    #
    MCD_MACD = df["MCD_MACD"]
    MCD_GRADIENT = df["MCD_GRADIENT"]
    MCD_PRICE = df["MCD_PRICE"]
    MCD_TRADE = df["MCD_TRADE"]
    MCD_PROFIT = df["MCD_PROFIT"]
    MCD_RETURN = df["MCD_RETURN"]
    #
    BA_MACD = df["BA_MACD"]
    BA_GRADIENT = df["BA_GRADIENT"]
    BA_PRICE = df["BA_PRICE"]
    BA_TRADE = df["BA_TRADE"]
    BA_PROFIT = df["BA_PROFIT"]
    BA_RETURN = df["BA_RETURN"]
    #
    CSCO_MACD = df["CSCO_MACD"]
    CSCO_GRADIENT = df["CSCO_GRADIENT"]
    CSCO_PRICE = df["CSCO_PRICE"]
    CSCO_TRADE = df["CSCO_TRADE"]
    CSCO_PROFIT = df["CSCO_PROFIT"]
    CSCO_RETURN = df["CSCO_RETURN"]
    #
    NKE_MACD = df["NKE_MACD"]
    NKE_GRADIENT = df["NKE_GRADIENT"]
    NKE_PRICE = df["NKE_PRICE"]
    NKE_TRADE = df["NKE_TRADE"]
    NKE_PROFIT = df["NKE_PROFIT"]
    NKE_RETURN = df["NKE_RETURN"]
    #
    JPM_MACD = df["JPM_MACD"]
    JPM_GRADIENT = df["JPM_GRADIENT"]
    JPM_PRICE = df["JPM_PRICE"]
    JPM_TRADE = df["JPM_TRADE"]
    JPM_PROFIT = df["JPM_PROFIT"]
    JPM_RETURN = df["JPM_RETURN"]
    #
    MRK_MACD = df["MRK_MACD"]
    MRK_GRADIENT = df["MRK_GRADIENT"]
    MRK_PRICE = df["MRK_PRICE"]
    MRK_TRADE = df["MRK_TRADE"]
    MRK_PROFIT = df["MRK_PROFIT"]
    MRK_RETURN = df["MRK_RETURN"]
    #
    CVX_MACD = df["CVX_MACD"]
    CVX_GRADIENT = df["CVX_GRADIENT"]
    CVX_PRICE = df["CVX_PRICE"]
    CVX_TRADE = df["CVX_TRADE"]
    CVX_PROFIT = df["CVX_PROFIT"]
    CVX_RETURN = df["CVX_RETURN"]

    for stock in allSymbols:
        priceCol="{}_PRICE".format(stock)
        macdCol="{}_MACD".format(stock)
        derivCol="{}_GRADIENT".format(stock)
        tradeCol="{}_TRADE".format(stock)
        profitCol="{}_PROFIT".format(stock)
        percentCol="{}_PCT_RTRN".format(stock)

    conn = sqlite3.connect('database')
    index = 0
    for (index < df.shape[1]):
        insert_into_TradingSignals(conn, dateAndTime, MSFT_MACD, MSFT_GRADIENT, MSFT_PRICE, MSFT_TRADE, MSFT_PROFIT, MSFT_RETURN,
        KO_MACD, KO_GRADIENT, KO_PRICE, KO_TRADE, KO_PROFIT, KO_RETURN,
        XOM_MACD, XOM_GRADIENT, XOM_PRICE, XOM_TRADE, XOM_PROFIT, XOM_RETURN,
        INTC_MACD, INTC_GRADIENT, INTC_PRICE, INTC_TRADE, INTC_PROFIT, INTC_RETURN,
        JNJ_MACD, JNJ_GRADIENT, JNJ_PRICE, JNJ_TRADE, JNJ_PROFIT, JNJ_RETURN,
        PG_MACD, PG_GRADIENT, PG_PRICE, PG_TRADE, PG_PROFIT,
        PFE_MACD, PFE_GRADIENT, PFE_PRICE, PFE_TRADE, PFE_PROFIT, PFE_RETURN,
        DIS_MACD, DIS_GRADIENT, DIS_PRICE, DIS_TRADE, DIS_PROFIT, DIS_RETURN,
        AXP_MACD, AXP_GRADIENT, AXP_PRICE, AXP_TRADE, AXP_PROFIT, AXP_RETURN,
        GS_MACD, GS_GRADIENT, GS_PRICE, GS_TRADE, GS_PROFIT, GS_RETURN,
        V_MACD, V_GRADIENT, V_PRICE, V_TRADE, V_PROFIT, V_RETURN,
        VZ_MACD, VZ_GRADIENT, VZ_PRICE, VZ_TRADE, VZ_PROFIT, VZ_RETURN,
        WMT_MACD, WMT_GRADIENT, WMT_PRICE, WMT_TRADE, WMT_PROFIT, WMT_RETURN,
        MCD_MACD, MCD_GRADIENT, MCD_PRICE, MCD_TRADE, MCD_PROFIT, MCD_RETURN,
        BA_MACD, BA_GRADIENT, BA_PRICE, BA_TRADE, BA_PROFIT, BA_RETURN,
        CSCO_MACD, CSCO_GRADIENT, CSCO_PRICE, CSCO_TRADE, CSCO_PROFIT, CSCO_RETURN,
        NKE_MACD, NKE_GRADIENT, NKE_PRICE, NKE_TRADE, NKE_PROFIT, NKE_RETURN,
        JPM_MACD, JPM_GRADIENT, JPM_PRICE, JPM_TRADE, JPM_PROFIT, JPM_RETURN,
        MRK_MACD, MRK_GRADIENT, MRK_PRICE, MRK_TRADE, MRK_PROFIT, MRK_RETURN,
        CVX_MACD, CVX_GRADIENT, CVX_PRICE, CVX_TRADE, CVX_PROFIT, CVX_RETURN)


    def insert_into_TradingSignals(connection, dateAndTime, MSFT_MACD, MSFT_GRADIENT, MSFT_PRICE, MSFT_TRADE, MSFT_PROFIT, MSFT_RETURN,
        KO_MACD, KO_GRADIENT, KO_PRICE, KO_TRADE, KO_PROFIT, KO_RETURN,
        XOM_MACD, XOM_GRADIENT, XOM_PRICE, XOM_TRADE, XOM_PROFIT, XOM_RETURN,
        INTC_MACD, INTC_GRADIENT, INTC_PRICE, INTC_TRADE, INTC_PROFIT, INTC_RETURN,
        JNJ_MACD, JNJ_GRADIENT, JNJ_PRICE, JNJ_TRADE, JNJ_PROFIT, JNJ_RETURN,
        PG_MACD, PG_GRADIENT, PG_PRICE, PG_TRADE, PG_PROFIT,
        PFE_MACD, PFE_GRADIENT, PFE_PRICE, PFE_TRADE, PFE_PROFIT, PFE_RETURN,
        DIS_MACD, DIS_GRADIENT, DIS_PRICE, DIS_TRADE, DIS_PROFIT, DIS_RETURN,
        AXP_MACD, AXP_GRADIENT, AXP_PRICE, AXP_TRADE, AXP_PROFIT, AXP_RETURN,
        GS_MACD, GS_GRADIENT, GS_PRICE, GS_TRADE, GS_PROFIT, GS_RETURN,
        V_MACD, V_GRADIENT, V_PRICE, V_TRADE, V_PROFIT, V_RETURN,
        VZ_MACD, VZ_GRADIENT, VZ_PRICE, VZ_TRADE, VZ_PROFIT, VZ_RETURN,
        WMT_MACD, WMT_GRADIENT, WMT_PRICE, WMT_TRADE, WMT_PROFIT, WMT_RETURN,
        MCD_MACD, MCD_GRADIENT, MCD_PRICE, MCD_TRADE, MCD_PROFIT, MCD_RETURN,
        BA_MACD, BA_GRADIENT, BA_PRICE, BA_TRADE, BA_PROFIT, BA_RETURN,
        CSCO_MACD, CSCO_GRADIENT, CSCO_PRICE, CSCO_TRADE, CSCO_PROFIT, CSCO_RETURN,
        NKE_MACD, NKE_GRADIENT, NKE_PRICE, NKE_TRADE, NKE_PROFIT, NKE_RETURN,
        JPM_MACD, JPM_GRADIENT, JPM_PRICE, JPM_TRADE, JPM_PROFIT, JPM_RETURN,
        MRK_MACD, MRK_GRADIENT, MRK_PRICE, MRK_TRADE, MRK_PROFIT, MRK_RETURN,
        CVX_MACD, CVX_GRADIENT, CVX_PRICE, CVX_TRADE, CVX_PROFIT, CVX_RETURN):
        c = connection.cursor()
        c.execute("insert into TransactionHistory values ({}, {}, {}, {}, '{}', {}, {}, \
        {}, {}, {}, '{}', {}, {}, \
        {}, {}, {}, '{}', {}, {}, \
        {}, {}, {}, '{}', {}, {}, \
        {}, {}, {}, '{}', {}, {}, \
        {}, {}, {}, '{}', {}, {}, \
        {}, {}, {}, '{}', {}, {}, \
        {}, {}, {}, '{}', {}, {}, \
        {}, {}, {}, '{}', {}, {}, \
        {}, {}, {}, '{}', {}, {}, \
        {}, {}, {}, '{}', {}, {}, \
        {}, {}, {}, '{}', {}, {}, \
        {}, {}, {}, '{}', {}, {}, \
        {}, {}, {}, '{}', {}, {}, \
        {}, {}, {}, '{}', {}, {}, \
        {}, {}, {}, '{}', {}, {},\
        {}, {}, {}, '{}', {}, {}, \
        {}, {}, {}, '{}', {}, {})".format( \
        dateAndTime.values[0], MSFT_MACD.values[0], MSFT_GRADIENT.values[0], MSFT_PRICE.values[0], MSFT_TRADE.values[0], MSFT_PROFIT.values[0], MSFT_RETURN.values[0], \
        KO_MACD.values[0], KO_GRADIENT.values[0], KO_PRICE.values[0], KO_TRADE.values[0], KO_PROFIT.values[0], KO_RETURN.values[0], \
        XOM_MACD.values[0], XOM_GRADIENT.values[0], XOM_PRICE.values[0], XOM_TRADE.values[0], XOM_PROFIT.values[0], XOM_RETURN.valeus[0], \
        INTC_MACD.values[0], INTC_GRADIENT.values[0], INTC_PRICE.values[0], INTC_TRADE.values[0], INTC_PROFIT.values[0], INTC_RETURN.values[0], \
        JNJ_MACD.values[0], JNJ_GRADIENT.values[0], JNJ_PRICE.values[0], JNJ_TRADE.values[0], JNJ_PROFIT.values[0], JNJ_RETURN.values[0], \
        PG_MACD.values[0], PG_GRADIENT.values[0], PG_PRICE.values[0], PG_TRADE.values[0], PG_PROFIT.values[0], \
        PFE_MACD.values[0], PFE_GRADIENT.values[0], PFE_PRICE.values[0], PFE_TRADE.values[0], PFE_PROFIT.values[0], PFE_RETURN.values[0], \
        DIS_MACD.values[0], DIS_GRADIENT.values[0], DIS_PRICE.values[0], DIS_TRADE.values[0], DIS_PROFIT.values[0], DIS_RETURN.values[0], \
        AXP_MACD.values[0], AXP_GRADIENT.values[0], AXP_PRICE.values[0], AXP_TRADE.values[0], AXP_PROFIT.values[0], AXP_RETURN.values[0], \
        GS_MACD.values[0], GS_GRADIENT.values[0], GS_PRICE.values[0], GS_TRADE.values[0], GS_PROFIT.values[0], GS_RETURN.values[0], \
        V_MACD.values[0], V_GRADIENT.values[0], V_PRICE.values[0], V_TRADE.values[0], V_PROFIT.values[0], V_RETURN.values[0], \
        VZ_MACD.values[0], VZ_GRADIENT.values[0], VZ_PRICE.values[0], VZ_TRADE.values[0], VZ_PROFIT.values[0], VZ_RETURN.values[0], \
        WMT_MACD.values[0], WMT_GRADIENT.values[0], WMT_PRICE.values[0], WMT_TRADE.values[0], WMT_PROFIT.values[0], WMT_RETURN.values[0], \
        MCD_MACD.values[0], MCD_GRADIENT.values[0], MCD_PRICE.values[0], MCD_TRADE.values[0], MCD_PROFIT.values[0], MCD_RETURN.values[0], \
        BA_MACD.values[0], BA_GRADIENT.values[0], BA_PRICE.values[0], BA_TRADE.values[0], BA_PROFIT.values[0], BA_RETURN.values[0], \
        CSCO_MACD.values[0], CSCO_GRADIENT.values[0], CSCO_PRICE.values[0], CSCO_TRADE.values[0], CSCO_PROFIT.values[0], CSCO_RETURN.values[0], \
        NKE_MACD.values[0], NKE_GRADIENT.values[0], NKE_PRICE.values[0], NKE_TRADE.values[0], NKE_PROFIT.values[0], NKE_RETURN.values[0], \
        JPM_MACD.values[0], JPM_GRADIENT.values[0], JPM_PRICE.values[0], JPM_TRADE.values[0], JPM_PROFIT.values[0], JPM_RETURN.values[0], \
        MRK_MACD.values[0], MRK_GRADIENT.values[0], MRK_PRICE.values[0], MRK_TRADE.values[0], MRK_PROFIT.values[0], MRK_RETURN.values[0], \
        CVX_MACD.values[0], CVX_GRADIENT.values[0], CVX_PRICE.values[0], CVX_TRADE.values[0], CVX_PROFIT.values[0], CVX_RETURN.values[0]
        ))
        connection.commit()
        i++


def main():
    allTickers=["MSFT", "KO", "XOM", "INTC", "JNJ", "PG", "PFE", "DIS", "AXP", "GS", "V", "VZ", "WMT", "MCD", "BA", "CSCO", "NKE", "JPM", "MRK", "CVX"]
    rng = makeTS();
    dataframe = makeDF(allTickers, rng);  #structure api call by passing in a ticker symbol
    dataframe.to_csv('./hasNullsExport.csv')
    cleanedDF = clean(dataframe)
    cleanedDF.to_csv('./cleanedExport.csv')
    results = analyze(cleanedDF, allTickers)
    #populateDB(cleanedDF, allTickers);#populate database with all time series data


#Tell python to call main function first
if __name__ == "__main__":
    main()
