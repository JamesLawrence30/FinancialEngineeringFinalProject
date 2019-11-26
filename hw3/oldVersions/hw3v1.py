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


def main():
    r1 = Rectangular(10,20)
    print(r1.area())
    print(r1.perimeter())

    s1 = Square(20)
    print(s1.area())
    print(s1.perimeter())

    return 0;

if __name__ == "__main__":
    main();
