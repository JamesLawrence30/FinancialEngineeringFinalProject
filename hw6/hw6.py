import sklearn
from sklearn import svm
from sklearn import linear_model
from sklearn import preprocessing
from sklearn.svm import SVC
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.model_selection import cross_val_score
from sklearn import datasets


#QUESTION 1

#Part 1
csv = 'points.csv'
points = pd.DataFrame(data=pd.read_csv(csv, low_memory=False));
x1 = pd.Series(points["x1"].tolist())
x2 = pd.Series(points["x2"].tolist())
plt.scatter(x1, x2)
plt.show()

clusters = KMeans(n_clusters=4)
prediction = clusters.fit_predict(points)
plt.scatter(x1, x2, c=prediction)
plt.show()


#Part 2
#Split into test and train
x1_train=x1[:-800]
x1_test=x1[-3200:]
x2_train=x2[:-800]
x2_test=x2[-3200:]

#Encoded data for classifying
encoder = preprocessing.LabelEncoder()
x1_train=encoder.fit_transform(x1_train).reshape(3200,-1)
x1_test=encoder.fit_transform(x1_test).reshape(3200,-1)
x2_train=encoder.fit_transform(x2_train).reshape(3200,-1)
x2_test=encoder.fit_transform(x2_test).reshape(3200,-1)

#Create SVM classifier and make predictions
clf = svm.SVC(kernel='linear')
model = clf.fit(x1_train,x2_train.ravel())
x2_pred = model.predict(x1_test)


#Create confusion matrix from predictions
print("Predictions:", x2_pred)
confusionMatrix = confusion_matrix(x2_test, x2_pred)
print("X2 Confusion Matrix:")
print(confusionMatrix)
confusionDF = pd.DataFrame(confusionMatrix)
confusionDF.to_csv('X2confusionMatrix.csv') #write confusion matrix to CSV

#Score the model
score = clf.score(x2_test, x2_pred)
print("X2 Score:", score)


#Part 3
csv = 'labels.csv'
labels = pd.DataFrame(data=pd.read_csv(csv, low_memory=False));
labels=labels[-3200:]
labels=encoder.fit_transform(labels).reshape(3200,-1)
print(labels)

confusionMatrix = confusion_matrix(labels, x2_pred)
print("Label Confusion Matrix:")
print(confusionMatrix)
confusionDF = pd.DataFrame(confusionMatrix)
confusionDF.to_csv('LabelconfusionMatrix.csv') #write confusion matrix to CSV

#Score the model
score = clf.score(labels, x2_pred)
print("Labels Score:", score)


#QUESTION 2
#Part 1
diabetesDATA = datasets.load_diabetes()

#Part 2
x_diab = diabetesDATA.data[:, np.newaxis, 2]
x_train = x_diab[:-20]
x_test = x_diab[-20:]

y_train = diabetesDATA.target[:-20]
y_test = diabetesDATA.target[-20:]

#Part 3
linearRegression = linear_model.LinearRegression()
linearRegression.fit(x_train, y_train) #data and target
y_prediction = linearRegression.predict(x_test) #predict target with data points

#Find the difference between the Truth values and the values we predict
coefficient = linearRegression.coef_
meanSquare = mean_squared_error(y_test, y_prediction)
Rsquare = r2_score(y_test, y_prediction)

print(coefficient)
print(meanSquare)
print(Rsquare)

#Part 4
kFold = 10
linRegr = linearRegression.fit(x_train, y_train) #data and target
kRange = [1,2,3,4,5,6,7,8,9,10]
for kValue in kRange:
    value = cross_val_score(linRegr, x_train, y_train, cv=10)
    print(value)


