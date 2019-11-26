myFirstString = 'first string!'
print(myFirstString)

student = "I'm a student"
print(student)

thoughts = """I enjoy this
course very much.  I think 
it will be informative and 
helpful in my career pursuits."""
print(thoughts)





a = 100
b = 9

c = a+b
print(c)

quotient = a/b
print(quotient)

quotINT = int(a/b)
print(quotINT)

remainder = a%b
print(remainder)

power = a**b
print(power)

DNE = a != b
print(DNE)

greater = a > b
print(greater)



#A is greater than 5 in length (length of 6) with int, float, string
A = [5, 2.5, "half", 3.5, 7, "double"]
print(A)

#define second list B
B = [10, 3.333, "third", 1.5, 6, "triple"]

#append B to original A
A.append(B)
print(A)

#re-define A to demonstrate an extend
A = [5, 2.5, "half", 3.5, 7, "double"]
A.extend(B)
print(A)

#second position in list is at index of 1 because index is 0, 1, 2, 3, ...
A.insert(1, "FE520")
print(A)

#pop second indexed item out of list A
A.pop(1)
print(A)

#get last element
print(A[-1])

#remove that last element
A.pop(-1)
print(A)

#new list from third indexed element 0, 1, 2, ... to end :]
C = A[2:]
print(C)

#double the size of C by comparing current length to double original length
originalLen = len(C)
while(len(C) < 2*originalLen):
    C.append('')
print(C)

C = C[::-1]
print(C)






DictA = {"name":"James", "age":20, "interests":"code"}
print(DictA)

DictB = dict(DictA)
print(DictB)
DictB.pop("name")
print(DictB)
print(DictA)




def listAdder(mylist, num):
    position = 0
    for value in mylist:
        if(position + 1 == len(mylist) and  num >= value):
            mylist.insert(position+1, num)
        elif(value <= num):
            position += 1
        else:
            mylist.insert(position, num)
            break;
    return mylist


print(listAdder([1, 2 , 4 , 9 , 17 , 25 , 63 ], 13))
