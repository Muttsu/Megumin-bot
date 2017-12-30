import sys

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class test(metaclass=Singleton):
    def __init__(self):
        self.stream = ""

    def write(self, s):
        self.stream = self.stream + s
        print(self.stream, file=sys.__stdout__)

    def flush(self):
        self.stream = ""

test = test()
sys.stdout = test

test.write("hi")
test.write("am cow")
