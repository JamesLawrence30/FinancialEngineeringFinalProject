#from pandas import Series, DataFrame
from pandas import DataFrame, Series
import pandas as pd
import numpy as np
from numpy import nan as NA

#QUESTION 1
creditcards = 'res_purchase_2014.csv'
data = pd.DataFrame(pd.read_csv(creditcards, low_memory=False))

#1)
dataframe = data['Amount'].astype(str) #convert to string to strip junk characters
dataframe = dataframe.map(lambda x: x.replace('$','').replace(')','').replace('zero','')) #remove problem characters
dataframe = dataframe.map(lambda x: x.replace('(', '-')) #negate values
dataframe = dataframe.astype(float) #convert strings to float
allAmount = dataframe.sum().round(2)
print("Full Total = ", allAmount)

#2
grainger = data.loc[data['Vendor'] == 'WW GRAINGER']
dataframe = grainger['Amount'].astype(str) #convert to string to strip junk characters
dataframe = dataframe.map(lambda x: x.replace('$','').replace(')','').replace('zero','')) #remove problem characters
dataframe = dataframe.map(lambda x: x.replace('(', '-')) #negate values
dataframe = dataframe.astype(float) #convert strings to float
graingerSum = dataframe.sum().round(2)
print("Grainger Total = ", graingerSum)

#3
supercenter = data.loc[data['Vendor'] == 'WM SUPERCENTER']
dataframe = supercenter['Amount'].astype(str) #convert to string to strip junk characters
dataframe = dataframe.map(lambda x: x.replace('$','').replace(')','').replace('zero','')) #remove problem characters
dataframe = dataframe.map(lambda x: x.replace('(', '-')) #negate values
dataframe = dataframe.astype(float) #convert strings to float
supercenterSum = dataframe.sum().round(2)
print("Supercenter Total = ", supercenterSum)

#4
grocery = data.loc[data['Merchant Category Code (MCC)'] == 'GROCERY STORES,AND SUPERMARKETS']
dataframe = grocery['Amount'].astype(str) #convert to string to strip junk characters
dataframe = dataframe.map(lambda x: x.replace('$','').replace(')','').replace('zero','')) #remove problem characters
dataframe = dataframe.map(lambda x: x.replace('(', '-')) #negate values
dataframe = dataframe.astype(float) #convert strings to float
grocerySum = dataframe.sum().round(2)
print("Grocery Store Total = ", grocerySum)


#############################################################################


#QUESTION 2

#1) read and create dataframe
Energy = 'Energy.csv'
BalanceSheet = pd.DataFrame(pd.read_csv(Energy))

Rating = 'EnergyRating.csv'
Ratings  = pd.DataFrame(pd.read_csv(Rating))


#2) Drop column with more than 90% of values = 0
BalanceSheet = BalanceSheet.fillna(0)
BalanceSheet = BalanceSheet.replace({0:np.nan})
BalanceSheet = BalanceSheet.dropna( axis=1, thresh=BalanceSheet.shape[1]*0.9)

Ratings = Ratings.fillna(0)
Ratings = Ratings.replace({0:np.nan})
Ratings = Ratings.dropna(axis=1, thresh=Ratings.shape[1]*0.9)


#3) Fill nan's with average of column
BalanceSheet = BalanceSheet.fillna(BalanceSheet.mean())
Ratings = Ratings.fillna(Ratings.mean())
###**might only want certain columns with numbers not columns??**


#4) Normalize dataframes
#(np.abs(x) - np.abs(x).max()) / (np.abs(x).max - np.abs(x).min())
BalanceSheet = (np.abs(BalanceSheet) - np.abs(BalanceSheet).max()) / (np.abs(BalanceSheet).max - np.abs(BalanceSheet).min())
#BalanceSheet.apply(n)
print(BalanceSheet)
