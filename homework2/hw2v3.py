import string
import math

def looper(originalHeight, landings):
    bounces = landings; #placeholder for the output string printed
    totalMeters = originalHeight; #initialize counter with value of original height
    while(landings > 0):
        originalHeight *= 0.25; #decrement original height by 1/4 on each bounce
        totalMeters += originalHeight; #increase meters bounced by the 1/4 height added by each bounce
        landings -= 1; #decrease remaining landings by 1 after each bounce

    print("After landing {} times, the ball bounces {} meters.".format(bounces, totalMeters))
    return originalHeight;


def stringer(inputStr):
    splitUp = inputStr.split(); #split string up into list of all words
    wordDict={};

    for word in splitUp: #step through list of words
        noPunct = word.lower(); #initialize a place holder for each word that has no punctuation
        if noPunct[0] in string.punctuation: #check if word starts with punctuation
            noPunct = noPunct.replace(noPunct[0], '');
        if noPunct[0] in string.punctuation: #check if word still starts with punctuation
            noPunct = noPunct.replace(noPunct[0], '')
        if noPunct[-1] in string.punctuation: #check if word ends with punctuation
            noPunct = noPunct.replace(noPunct[-1], '');
        if noPunct[-1] in string.punctuation: #check if word still ends with punctuation
            noPunct = noPunct.replace(noPunct[-1], '')
        
        #check if the word is already in the dictionary
        if noPunct in wordDict:
            for name,token in wordDict.items(): #step through name, token pairs already in dict to find the word you want to increment
                if name == noPunct:
                    token += 1;
                    wordDict[name] = token; #reassign the token value incremented 1 higher
        else:
            wordDict[noPunct] = 1; #if word is not already in the dictionary, add it with a token of 1
    
    maximum = max(wordDict, key = wordDict.get);
    print("The most frequent key is '{}', its frequency is {}.".format(maximum, wordDict[maximum]));
    return wordDict;


def eulerVersionOne(lambdaEqn,Yzero, deriv, Xzero, step, stop):
    zeroPoint = 0;
    while ((Yzero + ((Xzero+step)-Xzero)*deriv) - Yzero) < stop:
        zeroPoint = (Xzero+step);
        step+=step;
    print("for X0={}, the zero point of lambda function {} is {}".format(Xzero, lambdaEqn, zeroPoint));
    return zeroPoint;

def eulerVersionTwo(lambdaY, step, stop):
    Xzero = -4.000;
    x = Xzero;
    lastX = x;
    lastY = x*math.sin(x)-1;
    while x <= 4.000:
        currentY = x*math.sin(x)-1;
        x += step;
        deriv = (currentY-lastY)/(x-lastX)
        lastY = currentY;
        lastX = x;
    #    print(step*deriv);
        if step*deriv > stop: #y0 and x0 cancel out in the equation so I only account for h and derivative
            print(-4+x);


def main():
    print("\n");

    metersAfterBounce = looper(5000, 5);
    print(metersAfterBounce);
    print("\n");
    
    #############################################################

    myString = '''
    This course is designed for those students have no experience or
    limited experience on Python. This course will cover the basis
    syntax rules, modules, importing packages (Numpy, pandas), data
    visualization, and Intro for machine learning on Python. You will
    need to implement what you learn from this course to do a finance
    related project. This course aims to get you familiar with Python
    language, and can finish a simple project with Python.
    '''
    ret = stringer(myString);
    print(ret);
    print("\n");
    
    ############################################################33
    
    Xzero = -5;
    Yzero = 2*Xzero+4;
    lambdaY = "2x+4";
    derivative = 2; #since lambda is 2x+4
    stop = .001;
    step = stop**2; #stepping by E value squared for maimum precision
    zeroValue = eulerVersionOne(lambdaY,Yzero,derivative,Xzero,step,stop);
    print(zeroValue);
    print("\n");

    Xzero = 0;
    Yzero = 2*Xzero+4;
    lambdaY = "2x+4";
    derivative = 2; #since lambda is 2x+4
    stop = .001;
    step = stop**2; #stepping by E value squared for maimum precision
    zeroValue = eulerVersionOne(lambdaY,Yzero,derivative,Xzero,step,stop);
    print(zeroValue);
    print("\n");
    
    lambdaY = "x*sin(x)-1";
    stop = .001;
    step = .1; #stepping by .1 since E value squared takes too long to run
    print("The zero values of {} are:".format(lambdaY));
    eulerVersionTwo(lambdaY, step, stop);
    print("\n");

if __name__ == "__main__":
    main();
