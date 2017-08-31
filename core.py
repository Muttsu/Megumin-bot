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
        self.ignore_carry = kwargs.pop("ignore_carry", False)
        self.key_aliases = kwargs.pop("key_aliases", {})
        
    async def __call__(self, *args, **kwargs):
        args = list(args)
        carry = kwargs.pop("carry", None)
                
        if self.ignore_kwargs:
            kwargs = {}
                
        else:
            kwargs.update(self.parse_args(args))
            if "arg" in kwargs:
                args = [kwargs.pop("arg")]

        if not self.ignore_carry and carry is not None:
            if args[0]:
                kwargs[self.parse_key_alias("carry")] = carry
            else:
                args[0] = carry
        
        if not self.ignore_ctx:
            args.insert(0, self.ctx)
        
        return await self.func(*args, **kwargs)

    
    def parse_args(self, arg):
        kwargs = {}
        if isinstance(arg, list):
            arg = arg[0]
        
        arg = " " + arg

        pos = arg.find(" -")
        if pos != -1 and not arg[pos:].startswith(" --"):
            args = re.findall("(\s+--.*$|(^\s+|\s+-)\S+.*?)(?=\s+-|\s*$)", arg)
            args = [*map(lambda tup: tup[0], args)]

            buff = []
            for a in args:
                tmp = a.strip()
                if tmp.startswith("-"):
                    key = tmp[1:].split()[0]
                    val = tmp[1:].replace(key, "", 1).strip() or True

                    if tmp.startswith("--"):
                        a = tmp[1:].replace(key, "", 1)

                    elif key:
                        kwargs[self.parse_key_alias(key)] = val
                        continue

                buff.append(a)

            kwargs["arg"] = "".join(buff).strip()

        return kwargs
    
    def parse_key_alias(self, key):
        # Alias of an Alias
        if key in self.key_aliases:
            return self.parse_key_alias(self.key_aliases[key])
        # We found the key!
        else:
            return key
    
    

class Context:
    def __init__(self, **kwargs):
        self.message = kwargs.pop("message", None)
        self.bot = kwargs.pop("bot", None)
    
    async def say(self, msg):
        msg = msg.strip()
        if msg:
            return await self.bot.send_message(self.message.channel, msg)
        else:
            raise FunctionException("Cannot send empty message")


with open("config.json", "r") as f:
    secret = json.load(f)
    f.close()
    

class Start:
    def __init__(self, boolean = None):
        if boolean == "BOT":
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


