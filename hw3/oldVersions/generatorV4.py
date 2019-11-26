class LCG:
    seed = 0
    multiplier = 0
    increment = 0
    modulus = 0

    def __init__(self, seeds, mult, inc, mod):
        #defining the attributes
        self.seed = seeds
        self.multiplier = mult
        self.increment = inc
        self.modulus = mod
        print("seed:",self.seed," mult:",self.multiplier," inc:",self.increment," mod:",self.modulus)

    def getSeed(self):
        #return seed attribute
        return self.seed

    def setSeed(self, newseed):
        #set a new seed
        self.seed = newseed
        print("new seed set to:", self.seed)

    def initGen(self):
        #begin the number generation
        x0 = self.seed
        #calculate a random number with initial X
        p0 = x0/self.modulus
        return p0

    #function that contains LCG equation
    def equation(self, X):
        return ((self.multiplier*X)+self.increment)%self.modulus

    def nextRand(self):
        #print("X1 = (a*X0 + c) mod M =", x1)
        x0 = self.seed
        #pass in seed to get next number
        x1 = self.equation(x0)
        p1 = x1/self.modulus
        return p1

    def sequenceRand(self, length):
        sequence = [] #initialize an empty list for the random numbers
        x0 = self.seed
        p0 = self.initGen()
        sequence.append(p0) #populate the list with an initial random number

        if length < 1:
            #length cannot be 0 or negative
            return "Length must be greater than 0."
        elif length == 1:
            #we already started the list with one element so just return it
            return sequence
        else:
            for num in range(1,length):
                #create attidional X's by plugging in the previous X
                Xn = self.equation(x0)
                #points calculated dividing X/M
                Pn = Xn/self.modulus
                #add points to the list
                sequence.append(Pn) #add to the list as many times as the user calls for
                #increase the X to X+l for the next calculation of X+2
                x0 = Xn
        return sequence

class SCG(LCG):

    def initGen(self):
        if self.seed%4 !=2:
            #if condition not met, don't initialize the object
            raise ValueError('seed mod 4 should be 2')
        else:
            #I did not override this!!!! I only inherited it...fits the hint
            return LCG.initGen(self)
    
    def equation(self, X):
        #(Xn(Xn+1))mod M --> pass in the full equation of Xn with the parameter Xn+1 as a variable of
        return (((self.multiplier*(
            ((self.multiplier*(X+1))+self.increment)%self.modulus)
            )+self.increment)%self.modulus)%self.modulus


def main():
    v1 = LCG(0,1103515245,12345,2**32)
    print(v1.getSeed())
    v1.setSeed(1)
    print(v1.initGen())
    print(v1.nextRand())
    print(v1.sequenceRand(3))
    
    print("\n")

    v2 = SCG(1,1103515245,12345,2**32)
    print(v2.getSeed())
    v2.setSeed(6)
    print(v2.initGen())
    print(v2.nextRand())
    print(v2.sequenceRand(3))

if __name__ == "__main__":
    main()
