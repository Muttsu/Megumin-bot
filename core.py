import json
import re

commands = {}
aliases = {}

class FunctionException(Exception):
    pass

def command(name = None, **kwargs):
    def dec(fn):
        # add the command to dict
        nm = name or fn.__name__
        commands[nm] = Command(func = fn, **kwargs)

        return fn
    return dec


class Command:
    """Command Class to create.... New Commands!"""

    def __init__(self, *args, **kwargs):
        self.func = kwargs.pop("func", None)
        self.doc = self.func.__doc__
        self.ctx = kwargs.pop("ctx", None)
        self.ignore_ctx = kwargs.pop("ignore_ctx", False)
        self.ignore_kwargs = kwargs.pop("ignore_kwargs", False)

        
    async def __call__(self, *args, **kwargs):
        args = list(args)
        if self.ignore_kwargs:
            kwargs = {}
        else:
            kwargs = self.parse_args(args)
            if "arg" in kwargs:
                args = [kwargs.pop("arg")]
        
        if not self.ignore_ctx:
            args.insert(0, self.ctx)

        return await self.func(*args, **kwargs)

    
    def parse_args(self, arg):
        kwargs = {}
        if isinstance(arg, list):
            arg = arg[0]
        
        if arg.startswith("-"):
            arg = " " + arg

        pos = arg.find(" -")
        if pos != -1 and not arg[pos:].startswith(" --"):
            args = re.findall("(\s+--.*$|(^\s+|\s+-)\S+.*?)(?=\s+-|\s*$)", arg)
            args = map(lambda tup: tup[0], args)

            buff = []
            for a in args:
                tmp = a.strip()
                if tmp.startswith("-"):
                    key = tmp[1:].split()[0]
                    val = tmp[1:].replace(key, "", 1).strip() or True

                    if tmp.startswith("--"):
                        a = tmp[1:].replace(key, "", 1)

                    elif key:
                        kwargs[key] = val
                        continue

                buff.append(a)

            kwargs["arg"] = "".join(buff).strip()

        return kwargs
    
    

class Context:
    def __init__(self, **kwargs):
        self.message = kwargs.pop("message", None)
        self.bot = kwargs.pop("bot", None)
    
    async def say(self, msg):
        return await self.bot.send_message(self.message.channel, msg)


with open("config.json", "r") as f:
    secret = json.load(f)
    f.close()
    

class Start:
    def __init__(self, boolean = None):
        if boolean == "BOT":
            print("Made by Muttsu and twl")
            boolean = False
        self.state = bool(boolean)
    
    def __bool__(self):
        return self.state
    
    def __call__(self):
        self.state = True
        
#class Stack(*args):
#    def __init__(self, obj):
#        self.stack = list(args)
#    
#    def __call__(obj = None):
#        if obj is not None:
#            self.stack.append(obj)
#        else:
#            return self.stack.pop()


