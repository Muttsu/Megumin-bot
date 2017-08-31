import json
import re
from datetime import datetime


def command(name = None, **kwargs):
    def dec(fn):
        # add the command to dict
        nm = name or fn.__name__
        commands[nm] = Command(func = fn, **kwargs)

        return fn
    return dec


# == Config File ==
with open("config.json", "r") as f:
    secret = json.load(f)
    f.close()
commands = {}
aliases = {}
admin_ids = []


# == Exceptions ==
class FunctionException(Exception):
    pass


# == Classes ==
class Command:
    """Command Class to create.... New Commands!"""

    def __init__(self, *args, **kwargs):
        self.func = kwargs.pop("func", None)
        self.doc = self.func.__doc__
        self.ctx = kwargs.pop("ctx", None)

        self.ignore_all = kwargs.pop("ignore_all", False)

        self.ignore_ctx = kwargs.pop("ignore_ctx", self.ignore_all)
        self.ignore_kwargs = kwargs.pop("ignore_kwargs", self.ignore_all)
        self.ignore_carry = kwargs.pop("ignore_carry", self.ignore_all)
        self.ignore_args = kwargs.pop("ignore_args", self.ignore_all)

        self.key_aliases = kwargs.pop("key_aliases", {})
        self.key_aliases.update({"-s":"-silent", "-r":"-repeat"})

    async def __call__(self, *args, **kwargs):
        args = list(args)
        ctx = Context(ctx = self.ctx)
        carry = kwargs.pop("carry", None)
        args_dict = parse_args(args, self.key_aliases)

        ctx.silent = args_dict.pop("-silent", None)
        repeat = int(args_dict.pop("-repeat", 1))
        if repeat < 1:
            repeat = 1

        if self.ignore_kwargs or self.ignore_all:
            kwargs = {}

        else:
            kwargs.update(args_dict)
            if "arg" in kwargs:
                args = [kwargs.pop("arg")]

        if not self.ignore_carry and carry is not None:
            if args[0] or self.ignore_args:
                kwargs[parse_alias("carry", self.key_aliases)] = carry
            else:
                args[0] = carry

        if not self.ignore_ctx:
            args.insert(0, ctx)

        if self.ignore_args:
            args.pop()

        for _ in range(repeat):
            if self.ctx.message.author.id not in admin_ids and self.ctx.count > 7:
                raise Exception("Command cap reached")
            self.ctx.count += 1

            if self.ctx.bot.commands_enabled:
                r = await self.func(*args, **kwargs)
            else:
                raise Exception("Commands disabled")
        return r


class Context:
    def __init__(self, **kwargs):
        ctx = kwargs.pop("ctx", None)
        if ctx is None:
            self.message = kwargs.pop("message", None)
            self.bot = kwargs.pop("bot", None)
            self.silent = kwargs.pop("silent", None)
            self.current = kwargs.pop("current", ["Context declared"])
            self.count = kwargs.pop("count", 0)

            self.thread = [Thread()]
        elif isinstance(ctx, Context):
            self.bot = ctx.bot
            self.message = ctx.message

    async def say(self, msg):
        if not self.silent:
            msg = msg.strip()
            if msg:
                return await self.bot.send_message(self.message.channel, msg)
            else:
                raise FunctionException("Cannot send empty message")
        else:
            return None

    def new_thread(self, **kwargs):
        if len(self.thread) >= 2**8:
            raise Exception("Max Thread number reached")

        self.thread.append(Thread(**kwargs))
        return len(self.thread) - 1


class Thread:
    def __init__(self, **kwargs):
        self.stack = kwargs.pop("stack", [])
        self.command = kwargs.pop("command", "")
        self.carry = kwargs.pop("carry", Start())


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


# == parse functions ==
async def parse_message(ctx):
    """Removes Prefixes and Passes the Command to parse_command()"""

    content = ctx.message.content
    for pfx in ctx.bot.prefix:
        if content.startswith(pfx):
            # Remove prefix from message
            command = content.replace(pfx, "", 1).strip()
            break

    try:
        await parse_command(ctx, command)

    # Error parsing (◕‿◕✿)
    except FunctionException as e:
        log(ctx.message.author, "FUNCTION EXPLODED", ctx.current[-1], e)
        await ctx.say("<@{a}>, <@{a}>. Is this normal?```\n> {e}\n```"
            .format(a=ctx.message.author.id, e=str(e)))

    except Exception as e:
        log(ctx.message.author, "ERROR", ctx.current[-1], e)
        await ctx.say("<@{a}>, this is NOT how it works. ಠ_ಠ```\n> {e}```"
            .format(a=ctx.message.author.id, e=str(e)))

        # So I don't get depressed (◕‿◕✿)
        #if message.author.id in admin_ids:
        #    await bot.send_message(message.channel, "Aww")
        #else:
        #    await bot.send_message(message.channel, "Something went wrong and you're the cause. You suck.")


async def parse_command(ctx, command, thread = None):
    """Parse commands"""
    if ctx.bot.commands_enabled:
        ctx.current.append("parse_command: " + command)
        cmds = command.split(" & ")

        for cmd in cmds:
            if thread is None:
                thread = ctx.new_thread(command = command)

            cmd = cmd.split(" | ")
            for c in cmd:
                r = await execute(ctx, c, thread)
                ctx.thread[thread].stack.append(r)
                ctx.thread[thread].carry()
        return r


async def execute(ctx, command, thread):
    ctx.current.append("execute: " + command)
    command = command.strip()
    func_name = command.split(" ", 1)[0]
    arg = command.replace(func_name, "", 1).strip()

    if command:
        if func_name in aliases:
            return await parse_command(ctx,
                "{} {}".format(parse_alias(func_name), arg), thread)

        # Check if the command actually exists
        elif func_name in commands:
            func = commands[func_name]
            # Smartz way to pass bot and message objects
            func.ctx = ctx

            if ctx.thread[thread].carry:
                carry = ctx.thread[thread].stack.pop()
            else:
                carry = None

            r = await func(arg, carry = carry)

            # Log the return value
            log(ctx.message.author, "SUCCESS", command, r)
            return r

        else:
            raise Exception("'{}': not a command".format(func_name))


def parse_args(arg, als):
    kwargs = {}
    if isinstance(arg, list):
        arg = arg[0]

    arg = " " + arg

    pos = arg.find(" -")
    if pos != -1:
        args = re.findall("(\s+--\s+.*$|(^\s+|\s+-)\S+.*?)(?=\s+-|\s*$)", arg)
        args = [*map(lambda tup: tup[0], args)]

        buff = []
        for a in args:
            tmp = a.strip()
            if tmp.startswith("-"):
                key = tmp[1:].split()[0]
                val = tmp[1:].replace(key, "", 1).strip() or True

                if key:
                    if key == "-":
                        a = tmp[1:].replace(key, "", 1)
                    else:
                        kwargs[parse_alias(key, als)] = val
                        continue

            buff.append(a)

        kwargs["arg"] = "".join(buff).strip()

    return kwargs


def parse_alias(key, als):
    # Alias of an Alias
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

#class Stack(*args):
#    def __init__(self, obj):
#        self.stack = list(args)
#
#    def __call__(obj = None):
#        if obj is not None:
#            self.stack.append(obj)
#        else:
#            return self.stack.pop()


