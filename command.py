import asyncio

commands = {}

def command(name=None):
    def wrapper(fn):
        # add the command to dict
        nm = name or fn.__name__
        commands[nm] = Command(nm, fn)

        return fn
    return wrapper

class Command:
    def __init__(self, name, func, **kwargs):
        self.name = name
        self.func = func
        self.module = func.__module__