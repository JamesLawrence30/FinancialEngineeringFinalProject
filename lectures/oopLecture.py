"""
x = 'abc'
print(type(x));

y = list();
print(type(y));
"""

"""
"""
"""
class ClassName:
    <statement - 1>
    .
    .
    .
    <statemnet - N>
"""

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

"""
#cerated before adding parameter Name to constructor:

an = PartyAnimal()
print(an.x); #prints x declared as 0 no function party() run
an.party() #run party() and increment 1 before printing
an.party()
an.party()

print(dir(an)); # the things you can do with the class

an = 0;
an = PartyAnimal();
an.party()
an.party()
an = 42; #integer being assigned to the object..constructed
print('an contains ', an)
"""

s = PartyAnimal("Sally")
j = PartyAnimal("Jim")
s.party(2)
j.party(2)
s.party(2)
