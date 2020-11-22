class User:
    def __init__(self, name, email):
        self._name = name
        self._email = email
    
    def get_name(self):
        return self._name
    
    def get_email(self):
        return self._email

    def do_something(self):
        pass # placeholder for future code, nothing happens, avoids error when empty code is not allowed
        # raise ValueError() # possible a way to raise exception to find the problem

    def __str__(self):
        return self._name + ', ' + self._email

users =[ User('Testuser', 'testmail@mail.com'), User('User2','user2@mail.com')]

for user in users:
    user.do_something()