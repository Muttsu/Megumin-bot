"""This module contains all the stuff"""
import json
import re
import inspect
from datetime import datetime
import discord

bot = discord.Client() # pylint: disable=C0103

# == Config File ==
with open("config.json", "r") as f:
    CONFIG = json.load(f)
    f.close()

ADMIN_IDS = CONFIG["admins"]
ALIASES = CONFIG["aliases"]
COMMANDS = {}
MODULES = CONFIG["modules"]
PREFIX = CONFIG["prefix"]
if isinstance(PREFIX, str):
    PREFIX = [PREFIX]
TOKEN = CONFIG["token"]

if "commands_enabled" in CONFIG:
    bot.commands_enabled = CONFIG["commands_enabled"]
else:
    bot.commands_enabled = True


# == Exceptions == TO BE MOVED TO A NEW FILE ==
class FunctionException(Exception):
    """Custom exception implementation"""
    pass


# == Command Decorator ==
def command(**kwargs):
    """Additional parameter to be given to the decorator"""
    def dec(fct):
        """Command decorator to define commands"""
        args = inspect.getfullargspec(fct)[0]
        if "carry" not in args:
            kwargs["ignore_carry"] = True
        if "ctx" not in args:
            kwargs["ignore_ctx"] = True
        # add the command to dict
        name = kwargs.pop("name", fct.__name__)
        cmd = Command(func=fct, **kwargs)
        COMMANDS[name] = cmd
        return cmd
    return dec


# == Classes ==
#class Bot(discord.Client):
#    """helper class whith some usefull functions"""
#    def __init__(self, **kwargs):
#        discord.Client.__init__(self)
#        self.Commands = kwargs.pop("commands", {})
#        self.active_ctx = kwargs.pop("active_ctx",[])
#
#
#    async def reply(self, msg: str):
#        ctx = self.ctx(ctx_id = 0) #find a way to get ctx
#        if not ctx.silent:
#            msg = msg.strip()
#            if msg:
#                return await self.send_message(ctx.message.channel, msg)
#            else:
#                raise FunctionException("Cannot send empty message")
#        else:
#            return None
#
#
#    def new_ctx(self, **kwargs):
#        ctx = kwargs.pop("ctx", None)
#        self.active_ctx.append(ctx)
#        return len(self.active_ctx) - 1
#
#    def ctx(self, **kwargs):
#        ctx_id = kwargs.pop("ctx_id", len(self.active_ctx) - 1)
#        return self.active_ctx[ctx_id]



class Command:
    """Command Class to create.... New Commands!"""

    def __init__(self, *args, **kwargs):

        self.func = kwargs.pop("func", None)
        self.doc = self.func.__doc__

        self.ignore_all = kwargs.pop("ignore_all", False)

        self.ignore_args = kwargs.pop("ignore_args", self.ignore_all)
        self.ignore_kwargs = kwargs.pop("ignore_kwargs", self.ignore_all)

        self.ignore_ctx = kwargs.pop("ignore_ctx", self.ignore_all)
        self.ignore_carry = kwargs.pop("ignore_carry", self.ignore_all)

        self.key_aliases = kwargs.pop("key_aliases", None)

        self.opt_aliases = {"s":"silent", "r":"repeat", "v":"verbose"}


    async def __call__(self, *args, **kwargs):
        args = list(args)

        # take out the option kwargs
        ctx = kwargs.pop("ctx", None)
        carry= kwargs.pop("carry", None)
        ctx.silent = kwargs.pop("-silent", False)
        repeat = int(kwargs.pop("-repeat", 1))

        if repeat < 1:
            repeat = 1

        if self.ignore_args:
            args = []
        if self.ignore_kwargs:
            kwargs = {}

        # parse the alises for kwargs
        else:
            for key, val in kwargs.items():
                kwargs.pop(key)
                key = parse_alias(key, self.key_aliases)
                kwargs[key] = val

        if not self.ignore_ctx and ctx is not None:
            args.insert(0, ctx)
        if not self.ignore_carry and carry is not None:
            args.insert(1, carry)
        for _ in range(repeat):
            ret = await self.func(*args, **kwargs)
        return ret


class Context:
    """Object containing information about the executed command"""
    def __init__(self, **kwargs):
        self.message = kwargs.pop("message", None)
        self.bot = kwargs.pop("bot", None)
        self.current = kwargs.pop("current", ["Context Declared"])
        self.silent = kwargs.pop("silent", None)

        self.threads = kwargs.pop("threads", [])

    def new_thread(self):
        """creates a new thread and returns its index in the threads list"""
        if len(self.threads) >= 2**8:
            raise Exception("Max Thread number reached")
        self.threads.append([])
        return len(self.threads) - 1

    async def reply(self, msg):
        """Helper function"""
        if not self.silent:
            msg = msg.strip()
            if msg:
                return await self.bot.send_message(self.message.channel, msg)
            else:
                raise FunctionException("Cannot send empty message")
        else:
            return None


class Start:
    """retarded helper class"""
    def __init__(self, boolean = False):
        if boolean == "BOT":
            print("Made by Muttsu and twl")
            boolean = False
        self.state = bool(boolean)

    def __bool__(self):
        return self.state

    def __call__(self):
        self.state = True


# == parse functions == really should be inside Context? or not
async def parse_message(ctx):
    """Removes Prefixes and Passes the Command to parse_command()
    Also catches exceptions during execution of cmds"""

    content = ctx.message.content
    for pfx in PREFIX:
        if content.startswith(pfx):
            # Remove prefix from message
            content = content.replace(pfx, "", 1).strip()
            break

    try:
        await parse_command(ctx, content)

    # Error parsing (◕‿◕✿)
    except FunctionException as e:
        log(ctx.message.author, "FUNCTION EXPLODED", ctx.current[-1], e)
        await ctx.reply("<@{a}>, <@{a}>. Is this normal?```\n> {e}\n```"
            .format(a=ctx.message.author.id, e=str(e)))

    except Exception as e:
        log(ctx.message.author, "ERROR", ctx.current[-1], e)
        await ctx.reply("<@{a}>, this is NOT how it works. ಠ_ಠ```\n> {e}```"
            .format(a=ctx.message.author.id, e=str(e)))

    finally:
        del ctx


async def parse_command(ctx, content, thread_id = None):
    """Parse commands"""
    content = content.split(" & ")

    if thread_id is None:
        thread_id = ctx.new_thread()

    for cmds in content:
        cmds = cmds.split(" | ")
        for cmd in cmds:
            ret = await execute(ctx, cmd, thread_id)
            ctx.threads[thread_id].append(ret)
        ctx.new_thread()
    return ret


async def execute(ctx, cmd, thread_id):
    """execute"""
    cmd = cmd.strip()

    if cmd:
        func_name = cmd.split(" ", 1)[0]
        func_args = cmd.replace(func_name, "", 1).strip()

        if func_name in ALIASES:
            return await parse_command(ctx, parse_alias(func_name).format(func_args),thread_id)

        # Check if the command actually exists
        elif func_name in COMMANDS:
            func = COMMANDS[func_name]

            if ctx.threads[thread_id]:
                carry = ctx.threads[thread_id][-1]
            else:
                carry = None

            args, kwargs = parse_args(func_args)
            
            kwargs["carry"] = carry
            kwargs["ctx"] = ctx

            ret = await func(*args, **kwargs)

            # Log the return value
            log(ctx.message.author, "SUCCESS", cmd, ret)
            return ret

        else:
            #!!! rewrite exception
            raise Exception("'{}': not a command".format(func_name))


def parse_args(content:str):
    """Parse the arguments !!! does not parse key aliases; it must be done during the call of the command"""

    pattern = r"(\-[^\s]+\"[^\"\\]*(?:\\.[^\"\\]*)*\")|(\-[^\s]+\:[^\s]+)|(\-[^\s]+)|(\"[^\"\\]*(?:\\.[^\"\\]*)*\")|([^\s]+)"
    result = re.match(pattern, content)

    args = []
    kwargs = {}

    for match in re.finditer(r"\-([^\s\:\"]+)\s?(?:(\"[^\"\\]*(?:\\.[^\"\\]*)*)\"|([^\s]+))?", content):
        if match[0].startswith('"'):
            continue
        arg = match[2] or match[3]
        if arg:
            if arg[0] == arg[-1] == "\"":
                arg = arg[1:-1].strip()
            if re.fullmatch(r"\d+",arg) is not None:
                arg = int(arg)
            elif arg in ["True", "T", "t"]:
                arg = True
            elif arg in ["False", "F", "f"]:
                arg = False
            kwargs[match[1]] = arg
        else:
            kwargs[match[1]] = True
        content = content.replace(match[0], "", 1)

    for arg in re.findall(r"\"[^\"\\]*(?:\\.[^\"\\]*)*\"|\w+", content):
        if arg:
            if arg[0] == arg[-1] == "\"":
                arg = arg[1:-1].strip()
            if re.fullmatch(r"\d+",arg) is not None:
                arg = int(arg)
            elif arg in ["True", "T", "t"]:
                arg = True
            elif arg in ["False", "F", "f"]:
                arg = False
            args.append(arg)

    return args, kwargs


def parse_alias(key, als=None):
    # Alias of an Alias
    if als is None:
        als = ALIASES
    if key in als:
        return parse_alias(als[key], als)
    # We found the Alias
    else:
        return key


def log(author, state: str, message = "", info = None):
    """Logging, Logging, Error Debugging"""
    print("[{}] {:<20s}:{:<20s} {}".format(datetime.now().strftime("%H:%M:%S"), str(author), state, str(message)))
    if info:
        print("  > " + str(info))