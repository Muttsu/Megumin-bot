import asyncio

commands = {}

def command(name=None):
    def wrapper(fn):
        # add the command to dict
        nm = name or fn.__name__
        commands[nm] = Command(name = nm, func = fn)

        return fn
    return wrapper

class Command:
    def __init__(self, *args, **kwargs):
        self.name = kwargs.pop("name", None)
        self.func = kwargs.pop("func", None)
        self.ctx = kwargs.pop("ctx", None)
    
    async def __call__(self, *args, **kwargs):
        return await self.func(self.ctx, *args, **kwargs)
    
class Context:
    def __init__(self, **attrs):
        self.message = attrs.pop("message", None)
        self.bot = attrs.pop("bot", None)
    
    async def say(self, msg):
        return await self.bot.send_message(self.message.channel, msg)