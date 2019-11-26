from pandas import DataFrame, Series
import pandas as pd
import numpy as np
from numpy import nan

#QUESTION 1

#Bring csv into the python program
csv = 'HW5_Q1_data.csv';
data = pd.DataFrame(pd.read_csv(csv, low_memory=False));

#Clean the data
data = data.fillna(0); #fill blanks with 0
data = data.replace({0: np.nan}); #replace all 0 with NaN
data = data.dropna( axis=1, thresh=data.shape[1]*0.25) #drop cols with more than 25% NaN

print(data.head(10)); #print first 10 rows of cleaned data to confirm

#Downsample the daily data to monthly data
rng = pd.date_range(start='1/3/1990', end='11/1/1993', freq='D');

ts = pd.Series(len(data), index=rng);
print(ts.resample('M').mean());

"""
resmpld =  pd.Series(data['stock_0'].shape[1], index=rng);
print(resmpld.resample('M').mean());
"""
#ts = pd.Series(len(data), index=rng);
datastock1 = data['stock_0'];
#datastock1 = datastock1.resample('M').mean();
print(datastock1);
#print(ts);
"""
resampled = lambda x: x.resample('M').mean()
print(data.resampled);
"""
