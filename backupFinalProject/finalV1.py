import requests
import csv


alphaVantageKey = "0ZU6NM5CMUSMR7DO"

def makeRequest(symbol):
    #create api call string below. receive time series from api
    #datatype=csv is key here to receiving the data in a format that is useful for python
    csvURL = "https://www.alphavantage.co/query?function=MACD&symbol="+symbol+"&interval=1min&datatype=csv&series_type=open&apikey="+alphaVantageKey
    
    with requests.Session() as s:
        tSeriesDownload = s.get(csvURL); #make request and receive csv file

        decoded_content = tSeriesDownload.content.decode('utf-8'); #'decode' file to use as csv in python?
        
        tSeriesDecoded = csv.reader(decoded_content.splitlines(), delimiter=','); # turn csv into usable list in python?

        tSeriesWithHeader = list(tSeriesDecoded); #full csv file is now usable in python

        tSeries = tSeriesWithHeader[1:]; #remove first line off time series with name of each csv column

    return tSeries;


def populateDB(timeSeries):
    """
    for row in timeSeries:
        print(row)
    """
    for row in timeSeries:
        if(float(row[3]) >= 0.0):
            print("SELL: ", row[0], row[3]);
        if(float(row[3]) < 0.0):
            print("BUY: ", row[0], row[3]);

def main():
    timeSeries = makeRequest("CAT");  #structure api call by passing in a ticker symbol
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
