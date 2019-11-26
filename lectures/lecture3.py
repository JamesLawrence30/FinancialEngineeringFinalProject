import os
import pandas as pd
import numpy as np

def main():
#    print(dir("hello world\n")) #all the things you can do with this string..

    myString = "  My name is James   "
    myString.split(" ")

    myList = myString.split(" ") #the string has been converted to a list with the spli
    joinAndReplace = '***'.join(myList)
    print(joinAndReplace)


    print("my name is {name} and i am {age} years old".format(name="james", age="19"))

    """
    k = "dynamic variable"
    v = "903"
    print("the %k = %v, %d" % k, v, 6.0)
    """
    print(os.getcwd()) # current working directory
    print(np.array([1,2,3,4]))


if __name__ == "__main__":
    main()

