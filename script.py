import copy
print('hello world')


class Parent:
    def __init__(self, parent_name):
        self.parent_name = parent_name

    def parent_function(self):
        return self.parent_name

class Test(Parent):
    def __init__(self, name, qte, make):
        super().__init__(parent_name=name)
        self.qte = qte
        self.make = make

    def get_make(self):
        return self.make


test = Test('simon', 45, 'Rossignol')
print(help(Test))
print(test.get_make())
co = copy.deepcopy(test)



