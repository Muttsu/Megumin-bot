"""This module contains all the stuff"""
import re
import inspect
import asyncio
from datetime import datetime
from bot import bot
from dscio import dscin, dscout


COMMAND = re.compile(r'(?P<command>\w+)\s(?P<args>.*)')
ARGS = re.compile(r'(?P<dash>-{1,2})?(?(dash)(?P<key>[^\s=]+)(?P<eq>=)?|[\s$])?(?P<value>(?:\"[^\"\\]*(?:\\.[^\"\\]*)*\")|(?:[^\s]+))')


# == Command Decorator ==

def cmd(**kwargs):
    """Additional parameter to be given to the decorator"""
    def dec(fct):
        name = kwargs.pop("name", fct.__name__)
        cmd = Command(func=fct, **kwargs)
        bot.commands[name] = cmd
        # sub-commands to be implemented
        return cmd
    return dec


# == Classes ==
# TODO funcdoc
class Command:
    """"""

    def __init__(self, *args, **kwargs):
        self.func = kwargs.pop("func", None)
        self.doc = self.func.__doc__
        self.param = kwargs.pop("param", None)
        self.arg_aliases = kwargs.pop("key_aliases", None)


    async def __call__(self, ctx, *args, **kwargs):
        get_task().ctx = ctx
        return await self.func(*args, **kwargs)


    def _parse_arg(invoker):
        # TODO:
        args = []
        kwargs = {}

        return args, kwargs



def get_task():
    return asyncio.Task.current_task()


def parse_args(invoker: str):
    """Parse the arguments !!! does not parse key aliases; it must be done during the call of the command"""

    pattern = r"(\-[^\s]+\"[^\"\\]*(?:\\.[^\"\\]*)*\")|(\-[^\s]+\:[^\s]+)|(\-[^\s]+)|(\"[^\"\\]*(?:\\.[^\"\\]*)*\")|([^\s]+)"
    result = re.match(pattern, content)

    args = []
    kwargs = {}

    for match in re.finditer(r"\-([^\s\:\"]+)\:?(?:(\"[^\"\\]*(?:\\.[^\"\\]*)*)\"|([^\s]+))?", content):
        if match[0].startswith('"'):
            continue
        arg = match[2] or match[3]
        if arg:
            if arg[0] == arg[-1] == "\"":
                arg = arg[1:-1].strip()
            if re.fullmatch(r"\d+", arg) is not None:
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
            if re.fullmatch(r"\d+", arg) is not None:
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
        als = bot.aliases
    if key in als:
        return parse_alias(als[key], als)
    # We found the Alias
    else:
        return key


def log(author, state: str, message="", info=None):
    """Logging, Logging, Error Debugging"""
    print("[{}] {:<20s}:{:<20s} {}".format(datetime.now().strftime("%H:%M:%S"), str(author), state, str(message)))
    if info:
        print("  > " + str(info))


class Flag:
    def __init__()
