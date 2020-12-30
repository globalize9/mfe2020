class Person:
    '''this is a docustring'''
    age = 10

    def greet(self):
        print('Hello')

print(Person.age)
print(Person.greet)
print(Person.__doc__)


class ComplexNumber:
    def __init__(self, r=0, i=0):
        self.real = r
        self.imag = i

    def get_data(self):
        print(f'{self.real}+{self.imag}')

num1 = ComplexNumber(2,3)

num1.get_data()