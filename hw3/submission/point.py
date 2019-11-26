import math

class Point:
    x = 0
    y = 0
    
    def __init__(self, xval, yval):
        self.x = xval
        self.y = yval

    def distance(self):
        #distance formula
        d = math.sqrt((self.x-0)**2 + (self.y-0)**2)
        return d

