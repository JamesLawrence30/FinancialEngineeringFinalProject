"""
int('a');
int(123);

while True:
    try:
        x = int(input("please enter a number: "))
        break
    except ValueError: #can use except: if dont know error type
        print("oops not a valid number try again..")

"""

def input100(num):
    if type(num) != int:
        raise TypeError('input type should be an int! but is %s'%type(num))
    elif num != 100:
        raise ValueError('input is not 100..')
    else:
        return 'bingo'

#examples of the raise Error
"""
print(input100(100))
print(input100('x'))
print(input100(3))
"""

#try except prevents program from stopping
#no interruption from errors
try:
    a = input100('l')

except ValueError as info:
    print(info)
except TypeError as info:
    print(info)


