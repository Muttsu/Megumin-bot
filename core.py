import asyncio

commands = {}

def command(name=None, **kwargs):
    def wrapper(fn):
        # add the command to dict
        nm = name or fn.__name__
        commands[nm] = Command(name = nm, func = fn, **kwargs)

        return fn
    return wrapper

class Command:
    def __init__(self, *args, **kwargs):
        self.name = kwargs.pop("name", None)
        self.func = kwargs.pop("func", None)
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
    