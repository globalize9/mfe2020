# examples below are adapted from: https://www.programiz.com/python-programming/inheritance

class Person:
    '''this is a docustring'''
    age = 10

    def greet(self):
        print('Hello')

print(Person.age)
print(Person.greet)
print(Person.__doc__)


# In[]:
# Testing the complex number portion 
class ComplexNumber:
    def __init__(self, r=0, i=0):
        self.real = r
        self.imag = i

    def get_data(self):
        print(f'{self.real}+{self.imag}')

num1 = ComplexNumber(2,3)

num1.get_data()

num2 = ComplexNumber(5)
num2.attr = 10 # creating a new attribute 'attr'

print((num2.real, num2.imag, num2.attr))

# Attributes of an object can be deleted any time using the del statement
del num1.imag
# num1.get_data()

print((num2.real, num2.imag, num2.attr))
# automatic destruction of unreferenced objects in Python == garbage collection

# In[]:
# Class inheritance testing
print("\nClass inheritance testing\n")

class Polygon:
    def __init__(self, no_of_sides):
        self.n = no_of_sides
        self.sides = [0 for i in range(no_of_sides)]

    def inputSides(self):
        self.sides = [float(input("Enter side "+str(i+1)+" :")) for i in range(self.n)]

    def dispSides(self):
        for i in range(self.n):
            print("Side",i+1,"is",self.sides[i])

# test_P = Polygon(3)
# test_P.inputSides()
# test_P.dispSides()

class Triangle(Polygon):
    def __init__(self):
        Polygon.__init__(self,3)
        # __init__ defined here and in base class, this overrides it
        # however, this actually EXTENDS it, b/c of the above call

    def findArea(self):
        a,b,c = self.sides
        # calculate the semi-perimeter: half of its perimeter
        s = (a+b+c) / 2
        area = (s*(s-a)*(s-b)*(s-c)) ** 0.5
        print('The area of the triangle is %0.2f' %area)

t = Triangle()
t.inputSides()
t.dispSides()
t.findArea()

print(isinstance(t, Polygon))
print(isinstance(t,object))
print(isinstance(t,int))

print(issubclass(Polygon,Triangle))
print(issubclass(Triangle,Polygon))
# %%
# %%
