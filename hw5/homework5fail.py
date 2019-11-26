from pandas import DataFrame, Series
#from datetime import datetime
import datetime
import pandas as pd
import numpy as np
from numpy import nan

"""
#QUESTION 1

#Bring csv into the python program
csv = 'HW5_Q1_data.csv';
rawdata = pd.DataFrame(data=pd.read_csv(csv, low_memory=False));
#print(rawdata);


#Make index range and confirm it matches the Date column
rng = pd.bdate_range(start='1/3/1990', end='11/1/1993', freq='B'); #create our own range using business days
count = 0;
for date in rng:
	if str(date)[0:-9] != str(rawdata["Date"][count]):
		#print(str(date)[0:-9]) #this date is produced by our range, but not recorded in the dataset
		holiday=[str(date)[0:-9]] #set this date as a holiday to exclude from the new range
		break;
	count = count + 1


#Since the index range didn't match Date column, make a new range that does match
newrng = pd.bdate_range(start='1/3/1990', end='11/1/1993', holidays=holiday, freq='C', weekmask='Mon Tue Wed Thu Fri'); #remake range with the correct days


#Drop the original Date column to make room for custom index
data = rawdata.drop(columns="Date") #since we cannot index the original range, drop it and replace next..
#print(data);


#Make and apply custom index to the dataset
data["dates"] = newrng; #apply our own range to the dataset
#print(data);


#Clean the data
dataF = data.fillna(0); #fill blanks with 0
dataF = dataF.replace({0: np.nan}); #replace all 0 with NaN
dataF = dataF.dropna(axis=1, thresh=dataF.shape[1]*0.5)#drop col with more than 50% NaN
#print(dataF);


#Downsample to end-of-business-month and average the data to obtain each stock's average return over a month
monthly = dataF.resample('BM', on="dates").mean(); #using rng as an index, downsample dataF
#print(monthly)


#Average the rows to obtain average monthly return of all stocks in each month
monthly["avg"] = monthly.mean(axis=1) #average return of all stocks
#print(monthly["avg"])


#Find the change in returns between months and add it to an array
arr = [0];
psn = 0;
for returns in monthly["avg"]:
	if psn > 0: #go to the next position until you've reached the end of the column
		change = returns - monthly["avg"][psn-1]; #difference in returns between current month and the last month
		arr.append(change);
		#print(change);
	psn = psn + 1;


#Add the arry of changes in returns to the Data Frame
monthly["changes"] = arr;
#print(monthly["changes"]);


#Identify periods of Momentum and Mean Reversion in the changes in returns
array=["start"] #the first change is 0 and cannot indicate a trading strategy
counter = 1; #start at next position because of the first change being 0
for change in monthly["changes"]:
	# All the cases that indicate Momentum strategy
	if(monthly["changes"][counter+1] > 0 and monthly["changes"][counter] > 0): #if this change and next are positive
		array.append("Momen");
	elif(monthly["changes"][counter] > 0 and monthly["changes"][counter-1] > 0): #if this change and last were positive
		array.append("Momen");
	elif(monthly["changes"][counter+1] < 0 and monthly["changes"][counter] < 0): #if this change and next were negative
		array.append("Momen");
	elif(monthly["changes"][counter] < 0 and monthly["changes"][counter-1] < 0): #if this change and next were negative
		array.append("Momen");
	# Otherwise use Mean Reversion strategy
	else:
		array.append("Rever");

	# Once we've reached the end of the column, only look at the previous value so we don't go out of bounds
	counter = counter + 1;
	if counter == len(monthly["changes"])-1:
		if(monthly["changes"][counter] > 0 and monthly["changes"][counter-1] > 0):
			array.append("Momen");
		elif(monthly["changes"][counter] < 0 and monthly["changes"][counter-1] < 0):
			array.append("Momen");
		else:
			array.append("Rever");

		# break out of loop to avoid out of bounds
		break;
#print(array);


#Add the arry of changes in returns to the Data Frame
monthly["strategy"] = array;
#print(monthly[["changes","strategy"]]);


#Identify months that a change in strategy occurred and classify the change in strategy
current = 1;
changelog = ["start"]
for strat in monthly["strategy"]:
	#print(str(monthly["strategy"][current]) , str(monthly["strategy"][current-1]))
	if str(monthly["strategy"][current]) != str(monthly["strategy"][current-1]):
		changeString = "change "+monthly["strategy"][current-1]+" to "+monthly["strategy"][current];
		changelog.append(changeString);
	else:
		changelog.append("same");
	
	current = current + 1
	if current == len(monthly["strategy"]):
		break;
#print(changelog);


#Add the array of changes in returns to the Data Frame
monthly["stratChange"] = changelog;
#print(monthly[["changes","strategy","stratChange"]]);


#Output the last month that Momentum changed to Mean Reversion and vice versa
reverseStrats = monthly["stratChange"][::-1]; #reverse the column so I can find last entries easily
#print(reverseStrats)


# QUESTION 1 PART 1
#look through column for the first two changes (really the last two since column is flipped
psn=0;
count = 0;
for revStrat in reverseStrats:
	# If there was a strategy change
	if str(reverseStrats[psn]) != 'same':
		#print(monthly["stratChange"].iloc[[len(monthly["strategy"]) - psn-1]]); #print the date(month) and the change in strategy
		count = count + 1;
	psn=psn+1;

	if count == 2: #only print the last two changes, then stop
		break;


# QUESTION 1 PART 2
#print(monthly[["avg","strategy"]])
psn=0;
total=0;
count=0;
for strat in monthly["strategy"]:
	if str(strat) == 'Momen':
		#print(monthly["avg"][psn])
		total=total+monthly["avg"][psn]
		count=count+1;
	psn=psn+1;
#print("total returns during Momentum months: ",total)
#print("number of Momentum strategy months: ",count)
#print("average returns during Momentum strategy months:", total/count)


# QUESTION 1 PART 3
#print(monthly[["avg","strategy"]])
psn=0;
total=0;
count=0;
for strat in monthly["strategy"]:
	if str(strat) == 'Rever':
		#print(monthly["avg"][psn])
		total=total+monthly["avg"][psn]
		count=count+1;
	psn=psn+1;
#print("total returns during Mean Reversion months: ",total)
#print("number of Mean Reversion strategy months: ",count)
#print("average returns during Mean Reversion strategy months:", total/count)

"""
###################################################


#QUESTION 2

#Bring csv into the python program
csv = 'HW5_Q2_data.csv';
rawdata = pd.DataFrame(data=pd.read_csv(csv, low_memory=False, header=[0,1]));
#print(rawdata["SPX Index"]["Dates"]);
#print(rawdata["SPX Index"]["Dates"]);
psn=0
for day in rawdata["SPX Index"]["Dates"]:
	print(day[0:-day[::-1].index("/")+2])
	print(day[day[::-1].index("/")+1:])
	psn=psn+1



finalspxrng=[]
spxday = pd.bdate_range(start='7/30/2018 09:30:00', end='12/31/2018 16:00:00', freq='C', normalize=False, weekmask='Mon Tue Wed Thu Fri', tz='America/New_York'); #create our own range using 15 min intervals
#print(len(spxday))




spxrng = pd.bdate_range(start='7/30/2018 09:30:00', end='12/31/2018 16:00:00', freq='15T', normalize=False, tz='America/New_York'); #create our own range using 15 min intervals
#print(spxrng.summary())
spxstart = datetime.time(9,30,0);
spxend = datetime.time(16,0,0);
longdate = spxrng.date;
longtime = spxrng.time;
shortdate = rawdata["SPX Index"]["Dates"];
count=0;
for day in longdate:
	if day in shortdate:
		if longtime[count] >= spxstart:
			if longtime[count] <= spxend:
				print(spxrng[count])
				finalspxrng.append(spxrng[count])
	count = count+1
print(len(finalspxrng));







"""
# 1
#Drop the original Date columns to make room for custom indices
spx = rawdata["SPX Index"].drop(columns="Dates") #since we cannot index the original range, drop it and replace
print(spx);

sptsx = rawdata["SPTSX Index"].drop(columns="Dates")
print(sptsx);

ukx = rawdata["UKX Index"].drop(columns="Dates")
print(ukx);

dax = rawdata["DAX Index"].drop(columns="Dates")
print(dax);

cac = rawdata["CAC Index"].drop(columns="Dates")
print(cac);

hsi = rawdata["HSI Index"].drop(columns="Dates")
print(hsi);

nifty = rawdata["NIFTY Index"].drop(columns="Dates")
print(nifty);

nky = rawdata["NKY Index"].drop(columns="Dates")
print(nky);


#Clean the data
spx = spx.fillna(0); #fill blanks with 0
spx = spx.replace({0: np.nan}); #replace all 0 with NaN
spx = spx.dropna(axis=0) #drop row with an NaN
print(spx);

sptsx = sptsx.fillna(0); #fill blanks with 0
sptsx = sptsx.replace({0: np.nan}); #replace all 0 with NaN
sptsx = sptsx.dropna(axis=0) #drop row with an NaN
print(sptsx);

ukx = ukx.fillna(0); #fill blanks with 0
ukx = ukx.replace({0: np.nan}); #replace all 0 with NaN
ukx = ukx.dropna(axis=0) #drop row with an NaN
print(ukx);

dax = dax.fillna(0); #fill blanks with 0
dax = dax.replace({0: np.nan}); #replace all 0 with NaN
dax = dax.dropna(axis=0) #drop row with an NaN
print(dax);

cac = cac.fillna(0); #fill blanks with 0
cac = cac.replace({0: np.nan}); #replace all 0 with NaN
cac = cac.dropna(axis=0) #drop row with an NaN
print(cac);

hsi = hsi.fillna(0); #fill blanks with 0
hsi = hsi.replace({0: np.nan}); #replace all 0 with NaN
hsi = hsi.dropna(axis=0) #drop row with an NaN
print(hsi);

nifty = nifty.fillna(0); #fill blanks with 0
nifty = nifty.replace({0: np.nan}); #replace all 0 with NaN
nifty = nifty.dropna(axis=0) #drop row with an NaN
print(nifty);

nky = nky.fillna(0); #fill blanks with 0
nky = nky.replace({0: np.nan}); #replace all 0 with NaN
nky = nky.dropna(axis=0) #drop row with an NaN
print(nky);
"""

#Custom time series date range to be added as index for each
#must use normalize=False to obtain custom start and end minutes, otherwise defaults to midnight (00:00:00)


#weekmask='Mon Tue Wed Thu Fri',
#, holidays=['2018-12-25','2018-01-15']
"""
finalspxrng=[]
spxday = pd.bdate_range(start='7/30/2018 09:30:00', end='12/31/2018 16:00:00', freq='C', normalize=False, weekmask='Mon Tue Wed Thu Fri', tz='America/New_York'); #create our own range using 15 min intervals
#print(len(spxday))
spxrng = pd.bdate_range(start='7/30/2018 09:30:00', end='12/31/2018 16:00:00', freq='15T', normalize=False, tz='America/New_York'); #create our own range using 15 min intervals
#print(spxrng.summary())
spxstart = datetime.time(9,30,0);
spxend = datetime.time(16,0,0);
longdate = spxrng.date;
longtime = spxrng.time;
shortdate = rawdata['SPX Index']['Dates'].date; ###################################################
count=0;
for day in longdate:
	if day in shortdate:
		if longtime[count] >= spxstart:
			if longtime[count] <= spxend:
				print(spxrng[count])
				finalspxrng.append(spxrng[count])
	count = count+1
print(len(finalspxrng));
"""
"""
sptsxrng = pd.date_range(start='7/30/2018 09:30:00', end='12/31/2018 16:15', freq='15T', normalize=False, tz='America/Toronto'); #create our own range using 15 min intervals
print(sptsxrng.summary())

ukxrng = pd.date_range(start='7/30/2018 3:00', end='12/31/2018 7:30', freq='15T', normalize=False, tz='Europe/London'); #create our own range using 15 min intervals
print(ukxrng.summary())

daxrng = pd.date_range(start='7/30/2018 3:00', end='12/28/2018 8:00', freq='15T', normalize=False, tz='Europe/Berlin'); #create our own range using 15 min intervals
print(daxrng.summary())

cacrng = pd.date_range(start='7/30/2018 3:00', end='12/31/2018 11:30', freq='15T', normalize=False, tz='Europe/Paris'); #create our own range using 15 min intervals
print(cacrng.summary())

hsirng = pd.date_range(start='7/29/2018 21:15', end='12/30/2018 23:00', freq='15T', normalize=False, tz='Asia/Hong_Kong'); #create our own range using 15 min intervals
print(hsirng.summary())

niftyrng = pd.date_range(start='7/29/2018 23:45', end='1/1/2019 4:45', freq='15T', normalize=False, tz='Asia/Calcutta'); #create our own range using 15 min intervals
print(niftyrng.summary())

nkyrng = pd.date_range(start='7/29/2018 20:00', end='12/28/2018 1:15', freq='15T', normalize=False, tz='Asia/Tokyo'); #create our own range using 15 min intervals
print(nkyrng.summary())
"""

#Make and apply custom index to the dataset
#print("spx: ", len(spx))
#print("spxrng: ", len(spxrng))
#for dt in spxrng:
#	print(dt)
spx["Dates"] = finalspxrng; #apply our own range to the dataset
#print(spx);