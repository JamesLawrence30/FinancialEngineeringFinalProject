def divide(x, y):
    try:
        result = x / y
    except: #the above try caused error
        print('division by zero!')
    else: #no exception raised by division
        print("result is ", result)
    finally:
        print("finally clause always executed")

print("\n------------")
divide(2,1)
print("------------")
divide(2,0)
print("------------")
divide("2","1")
print("------------")

