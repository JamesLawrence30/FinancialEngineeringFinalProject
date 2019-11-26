class LCG:
    seed = 0
    multiplier = 0
    increment = 0
    modulus = 0

    def __init__(self, seeds, mult, inc, mod):
        self.seed = seeds
        self.multiplier = mult
        self.increment = inc
        self.modulus = mod
        print("seed:",self.seed," mult:",self.multiplier," inc:",self.increment," mod:",self.modulus)

    def getSeed(self):
        return self.seed

    def setSeed(self, newseed):
        self.seed = newseed
        print("new seed set to:", self.seed)

    def initGen(self):
        x1 = ((self.multiplier*self.seed)+self.increment)%self.modulus
        #print("X1 = (a*X0 + c) mod M =", x1)
        x0 = 1/self.modulus
        return x0

    def nextRand(self):
        x1 = ((self.multiplier*self.seed)+self.increment)%self.modulus
        x2 = ((self.multiplier*x1)+self.increment)%self.modulus
        #print("X1 = (a*X0 + c) mod M =", x1)
        #print("X2 = (a*X1 + c) mod M =", x2)
        return x2

    def sequenceRand(self, length):
        sequence = []
        x1 = ((self.multiplier*self.seed)+self.increment)%self.modulus
        sequence.append(x1)

        if length < 1:
            return "Length must be greater than 0."
        elif length == 1:
            return sequence
        else:
            for num in range(2,length+1):
                Xn = ((self.multiplier*x1)+self.increment)%self.modulus
                sequence.append(Xn)
                x1 = Xn
        return sequence


def main():
    v1 = LCG(0,1103515245,12345,2**32)
    print(v1.getSeed())
    v1.setSeed(1)
    print(v1.initGen())
    print(v1.nextRand())
    print(v1.sequenceRand(5))

if __name__ == "__main__":
    main()
