class Human: #parent class
    def __init__(self, Name, Gender, Age):
        self.gender = Gender;
        self.age = Age;
        self.name = Name;

    def run(self):
        print('{name} is running.'.format(name=self.name))

class Student1(Human): #child class
    def study(self):
        print('%s is studying.' % self.name)

class Student2(Human):
    def run(self):
        print('i am a student..')
        Human.run(self)


student = Student1('David', 'male', 23)

print(student.gender)
print(student.age)
print(student.name)

#run is a function of class Human but student is a child of human so run can be called directly with student
student.run()
#study is a fct of student, using the name inherited from Human
student.study()

print(dir(student))

#the class in the child has higher priority than the parent
student = Student2('David', 'male', 23)
student.run()


