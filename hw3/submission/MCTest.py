from point import Point
from generatorV5 import LCG
from generatorV5 import SCG

#Using LCG generator
print("\nUsing LCG:")

LCGpoints = LCG(2,1103515245,12345,2**32)
#make sqrt(10 million) x values
xVals = LCGpoints.sequenceRand(3162)
#make sqrt(10 million) y values
LCGpoints = LCG(5,1103515245,12345,2**32)
yVals = LCGpoints.sequenceRand(3162)

counter = 0 #to count number of points inside the circle
#with make 10 million unique points using n^2 runtime
#due to nested for loop of sqrt(10 million) values each
for x in xVals:
    for y in yVals:
        myPoint = Point(x,y)
        if myPoint.distance() <= 1:
            counter = counter + 1

myRatio = counter/10000000
print("My ratio with LCG:", myRatio)

difference = abs(myRatio - 0.78539816339)
print("Difference pi/4 - my ratio:", difference)

print("\n\n\n")##################################################

#Using SCG generator
print("Using SCG:")

SCGpoints = SCG(10,1103515245,12345,2**32)
#make sqrt(10 million) x values
xVals = SCGpoints.sequenceRand(3162)
#make sqrt(10 million) y values
SCGpoints = SCG(14,1103515245,12345,2**32)
yVals = SCGpoints.sequenceRand(3162)

counter = 0 #to count number of points inside the circle
#with make 10 million unique points using n^2 runtime
#due to nested for loop of sqrt(10 million) values each
for x in xVals:
    for y in yVals:
        myPoint = Point(x,y)
        if myPoint.distance() <= 1:
            counter = counter + 1

myRatio = counter/10000000
print("My ratio using SCG:", myRatio)

difference = abs(myRatio - 0.78539816339)
print("Difference pi/4 - my ratio:", difference)

