import numpy as np

#parent class
class Rectangular:
    length = 0
    width = 0

    def __init__(self, leng, wid):
        self.length = leng
        self.width = wid
        print("\nInitialized rectangle of length:", self.length, "and width:", self.width)

    def area(self):
        a = self.length * self.width
        return a

    def perimeter(self):
        per = (2*self.length) + (2*self.width)
        return per

#child class of rectangular (5 points bonus :)
class Square(Rectangular):
    def __init__(self, lengt):
        #call constructor of the parent
        super().__init__(lengt, lengt)


class Time:
    hours = 0
    minutes = 0
    seconds = 0

    def __init__(self, hour, minute, second):
        self.hours = hour
        self.minutes = minute
        self.seconds = second
        print("\ninitialized with", self.hours, "hours,", self.minutes, "minutes, and", self.seconds, "seconds.")

    def addTime(self, newhour, newminute, newsecond):
        sumhours = self.hours + newhour + int((self.minutes+newminute)/60)#carry minutes over if minutes > 60
        #only want the leftover minutes that didnt carry over to a new hour
        summins = ((self.minutes + newminute)%60) + int((self.seconds+newsecond)/60)#carry seconds over if seconds > 60
        #only want the leftover seconds that didnt carry over to a new minute
        sumsecs = (self.seconds + newsecond)%60

        print(sumhours, "hr and", summins, "min and", sumsecs, "seconds.")

    def DisplayMinute(self):
        #displays the total seconds in the Time object
        sumhours = self.hours + int(self.minutes/60)#carry minutes over if minutes > 60
        #only want the leftover minutes that didnt carry over to a new hour
        summins = (self.minutes%60) + int(self.seconds/60)#carry seconds over if seconds > 60
        #only want the leftover seconds that didnt carry over to a new minute
        sumsecs = self.seconds%60

        totalSecs = (sumhours*60*60) + (summins*60) + sumsecs
        print(totalSecs)




def main():
    #   1.1
    r1 = Rectangular(10,20)
    print(r1.area())
    print(r1.perimeter())

    s1 = Square(20)
    print(s1.area())
    print(s1.perimeter())
    
    #   1.2
    array1 = 1,2,3,4,5,6,7,8,9,10
    array2 = 2,4,6,8,10,12,14,16,18,20
    arr1 = np.array(array1)
    arr2 = np.array(array2)
    
    numRect = Rectangular(arr1, arr2)
    print(numRect.area())
    print(numRect.perimeter())
    
    #   2
    t1 = Time(1,20,5)
    t1.addTime(2,50,10)
    t1.DisplayMinute()

    return 0;

if __name__ == "__main__":
    main();
