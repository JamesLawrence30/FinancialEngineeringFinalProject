
class PartyAnimal:
    x = 0;
    name = ''
    #must always define self in the first method of the class
    #construct all partyanimal classes with a name
    def __init__(self, nam): #constructor sets up initial values for the class..prepare for calculations in functions
        self.name = nam
        print(self.name, " I am constructed.")

    #y is a variable that must be passed into the function each time this function of the class is called
    def party(self, y): #self is a variable defined in the function...passed to the function since self used
        self.x = self.x+1+y
        print(self.name, " party count ", self.x)
    
    #destroying the class
    def __del__(self): # destructor
        print('destroy', self.x)


s = PartyAnimal("Sally")
j = PartyAnimal("Jim")
s.party(2)
j.party(2)
s.party(2)
