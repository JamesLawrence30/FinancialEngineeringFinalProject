import pandas as pd

#can only make 5 API calls per minute, and need to make 20, so had to download all the CSV files first

def makeRequest(symbol):
    #go to directory with all the csv files and pick the desired file
    csvLocation = './csvData/technical_indicator_{}.csv'.format(symbol)
    #turn the csv into a data frame with pandas
    dataFrame = pd.DataFrame(pd.read_csv(csvLocation, low_memory=False))
    cleanData = clean(dataFrame)
    return cleanData


def clean(rawDF):
    #do backfill for missing data or 0's?
    return rawDF #return the cleaned data eventually..


def populateDB(df):
    for index, row in df.iterrows():
        #need index, row to access row values by name
        if(float(row["MACD_Signal"]) >= 0.0):
            print("SELL:", row["time"], row["MACD_Signal"]);
        if(float(row["MACD_Signal"]) < 0.0):
            print("BUY:", row["time"], row["MACD_Signal"]);


def main():
    timeSeries = makeRequest("MSFT");  #structure api call by passing in a ticker symbol
    populateDB(timeSeries);#populate database with all time series data
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
