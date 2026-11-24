def add(a,b):
    return a+b

def sub(a,b):
    return a-b

print(__name__)

if __name__=="__main__":
    print("CALCULATOR")
    n1=int(input("enter num1:"))
    n2=int(input("enter num2:"))
    print("ADDITION:",add(n1,n2))
    print("SUBRACTION:",sub(n1,n2))
