import asyncio
import json
from datetime import datetime

commands = {}
aliases = {}

def command(name=None, **kwargs):
    def wrapper(fn):
        # add the command to dict
        nm = name or fn.__name__
        commands[nm] = Command(func = fn, **kwargs)

        return fn
    return wrapper

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


# == New Section ==
with open("config.json", "r") as f:
    secret = json.load(f)
    f.close()
if "aliases" in secret:
    aliases = secret[aliases]

async def parse_message(bot, message):
    """Transforms message content into an array of commands"""

    content = message.content
    for pfx in bot.prefix:
        if content.startswith(pfx):
            # Remove prefix from message
            commands = map(lambda string: string.strip(),
                # Split the commands
                content.replace(pfx, "", 1).split(" & "))
            break

    for cmd in commands:
            await parse_command(cmd, bot, message)


async def parse_command(command, bot, message):
    """Parse individual commands"""

    cmd = command.split(" ", 1)
    func = parse_alias(cmd[0])
    args = cmd[1:]

    

    # Check if the command actually exists
    if isinstance(func, Command):
        # Smartz way to pass bot and message objects
        func.ctx = Context(bot = bot, message = message)
        try:
            # Log the return value
            log(message.author, "SUCCESS", command,
                await func(*args))

        # Error parsing
        except Exception as e:
            log(message.author, "ERROR", command, e)
            await bot.send_message(message.channel, str(e))

            # So I don't get depressed (◕‿◕✿)
            if message.author.id in admin_ids:
                await bot.send_message(message.channel, "Aww")
            else:
                await bot.send_message(message.channel, "Something went wrong and you're the cause. You suck.")
    else:
        log(message.author, "ERROR", command, "'{}': not a command".format(func))
        
def parse_alias(func_name):
    # Alias of an Alias
    if func_name in aliases:
        return parse_alias(aliases[func_name])
    # We found the Function
    elif func_name in commands:
        return commands[func_name]
    else:
        return func_name


def log(author, state: str, message, info = None):
    """Logging, Logging, Error Debugging"""
    print("[{}] {:<20s}:{:<10s} {}".format(datetime.now().strftime("%H:%M:%S"), str(author), state, str(message)))
    if info:
        print("  > " + str(info))

class Start():
    def __init__(self):
        print("Made by Muttsu and twl")
        self.state = False
    
    def __nonzero__(self):
        return self.state
    
    def __call__(self):
        self.state = True
