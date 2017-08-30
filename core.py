import asyncio
import json
from datetime import datetime

commands = {}
aliases = {}

class FunctionException(Exception):
    pass

def command(name=None, **kwargs):
    def dec(fn):
        # add the command to dict
        nm = name or fn.__name__
        commands[nm] = Command(func = fn, **kwargs)

        return fn
    return dec

class Command:
    def __init__(self, *args, **kwargs):
        self.func = kwargs.pop("func", None)
        self.doc = self.func.__doc__
        self.ctx = kwargs.pop("ctx", None)
        self.ignore_ctx = kwargs.pop("ignore_ctx", False)

    async def __call__(self, *args, **kwargs):
        if self.ignore_ctx:
            return await self.func(*args, **kwargs)
        else:
            return await self.func(self.ctx, *args, **kwargs)

class Context:
    def __init__(self, **kwargs):
        self.message = kwargs.pop("message", None)
        self.bot = kwargs.pop("bot", None)
    
    async def say(self, msg):
        return await self.bot.send_message(self.message.channel, msg)


with open("config.json", "r") as f:
    secret = json.load(f)
    f.close()
    

class Start(boolean = False):
    def __init__(self, boolean):
        print("Made by Muttsu and twl")
        self.state = boolean
    
    def __bool__(self):
        return self.state
    
    def __call__(self):
        self.state = True


