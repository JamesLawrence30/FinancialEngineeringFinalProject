from pandas import DataFrame, Series
import pandas as pd
import numpy as np
from numpy import nan

#QUESTION 1

#Bring csv into the python program
csv = 'HW5_Q1_data.csv';
data = pd.DataFrame(data=pd.read_csv(csv, low_memory=False));
data = data.drop(columns="Date")

rng = pd.bdate_range(start='1/3/1990', periods=998, freq='B');#use business days
data["dates"] = rng;
print(data);

#rng = pd.date_range(start='1/3/1990', end='11/1/1993', freq='D');
#csvIn = pd.DataFrame(pd.read_csv(csv, low_memory=False), index=rng);
#print(csvIn);

#Clean the data
dataF = data.fillna(0); #fill blanks with 0
dataF = dataF.replace({0: np.nan}); #replace all 0 with NaN
dataF = dataF.dropna(axis=1, thresh=dataF.shape[1]*0.25)#drop col with more than 25% NaN
print(dataF); #print first 10 rows of cleaned data to confirm
monthly = dataF.resample('BM', on="dates").mean();
print(monthly)

#Downsample the daily data to monthly data
#rng = pd.bdate_range(start='1/3/1990', end='11/1/1993', freq='B');#use business days
#print(rng);
#using date_range gives too many days: sun-sat, instead of mon-fri
#still have 999 rows but need 998...


"""
for col in dataF.columns:
    ts = pd.Series(len(col), index=rng);
    print(ts.resample('M').mean());
"""


#datastock0 = dataF['stock_0'];
#print(datastock0.head(10));


#ts = pd.Series(dataF, index=rng);
###############df = pd.DataFrame(data=dataF, index=dataF["Date"]);
###############print(df);
#lamb = ts.groupby(lambda x: x.month).mean();
#print(df.head(10));

#monthly = csvIn.resample('M')#.mean();
#print(monthly);
###############print(df.resample('BM'));


"""
resampled = lambda x: x.resample('M').mean()
print(data.resampled);
"""
