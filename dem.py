class Person:
    def __init__(self, name):
        self.__name = name

    @property
    def do_something(self):
        return "Andy"

    @property
    def name(self):
        if len(self.__name) < 5:
            raise ValueError
        return self.__name


p = Person("Fred Bloggs")

print(p.name)
print(p.do_something)
# added this
# blah
