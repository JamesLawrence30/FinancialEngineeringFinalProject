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

print(BalanceSheet.head(10))
print(Ratings.head(10))


#3) Fill nan's with average of column
BalanceSheet = BalanceSheet.fillna(BalanceSheet.mean()) #fill numeric empty spaces with the average of their column
Ratings = Ratings.fillna(Ratings.mean()) #fill numeric empty spaces with the average of their column
#print(BalanceSheet.head(10))
#print(Ratings.head(10))


#4) Normalize dataframes
newX = lambda x: (x-x.min())/(x.max()-x.min()) #normal calculator function

BalanceSheetNums = BalanceSheet.select_dtypes([np.number]) #selecting numeric columns only to normalize
RatingsNums = Ratings.select_dtypes([np.number]) #selecting numeric columns only to normalize

normalBalanceSheet = BalanceSheetNums.apply(newX) #call normalize function
normalRatings = RatingsNums.apply(newX) #call normalize function

print(normalBalanceSheet.head(10))
print(normalRatings.head(10))


#5) Correlation
Energy = 'Energy.csv'
newBalanceSheet = pd.DataFrame(pd.read_csv(Energy)) #needed to make a new balance sheet since 'Assets Netting & Other Adjustments' was dropped earlier
bsCols = newBalanceSheet[['Current Assets - Other - Total', 'Current Assets - Total', 'Other Long-term Assets', 'Assets Netting & Other Adjustments']]

print(bsCols.corr())


#6) Name Column
BalanceSheet['Name'] = BalanceSheet['Company Name'].str.split().str[-1] #get last word of company name and store in new column called Name
print(BalanceSheet['Company Name']) #check company name
print(BalanceSheet['Name']) #check name

#7) Inner Join
Matched = pd.merge(Ratings, BalanceSheet, on=['Data Date', 'Global Company Key'], how='inner') #inner join on three keys
print(Matched.head(10))


#8) Ratings
def rateNum(psn): #check for a rating based on the position in the Rate column that we map through
    if psn == 'AAA':
        return 0
    elif psn == 'AA+':
        return 1
    elif psn == 'AA':
        return 2
    elif psn == 'AA-':
        return 3
    elif psn == 'A+':
        return 4
    elif psn == 'A':
        return 5
    elif psn == 'A-':
        return 6
    elif psn == 'BBB+':
        return 7
    elif psn == 'BBB':
        return 8
    elif psn == 'BBB-':
        return 9
    elif psn == 'BB+':
        return 10
    elif psn == 'BB':
        return 11
    elif psn == 'others': #others is 12
        return 12
    elif psn == '': #also a blank is 12
        return 12

Matched['Rate'] = Matched['S&P Domestic Long Term Issuer Credit Rating'].astype(str).map(lambda x: rateNum(x)) #store the rating number for every rate in new column
print(Matched['Rate'])


#9) Ratings Frequency
allCo = Matched.loc[Matched['Name'] == 'CO'] #select all rows that are a CO
print("Average Rating for CO's = ", allCo['Rate'].mean().round(2)) #average the rate numbers of all Co's


#10) Output file
Matched.to_csv('HW4.csv') #send finished csv to new file

