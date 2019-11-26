import string

def looper(originalHeight, landings):
    bounces = landings; #placeholder for the output string printed
    totalMeters = originalHeight; #initialize counter with value of original height
#    print(originalHeight);
    while(landings > 0):
        originalHeight *= 0.25; #decrement original height by 1/4 on each bounce
#        print(originalHeight)
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
                    #print(key);
                    token += 1;
                    wordDict[name] = token; #reassign the token value incremented 1 higher
                    #print(val);
        else:
            wordDict[noPunct] = 1; #if word is not already in the dictionary, add it with a token of 1
    
    #print(wordDict);
    maximum = max(wordDict, key = wordDict.get);
    print("The most frequent key is '{}', its frequency is {}.".format(maximum, wordDict[maximum]));
    return wordDict;


def findZero():
    print("find zero");


def main():
    metersAfterBounce = looper(5000, 5);
    print(metersAfterBounce)


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


    findZero();

if __name__ == "__main__":
    main();
