import asyncio
from datetime import datetime
import re

from core import *

@command()
async def help(ctx, func: str):
    """Displays the reference manual for commands and aliases
    Usage: help <func:str>"""
    
    if func in aliases:
        doc = "'{}' is an alias for '{}'".format(func, aliases[func])

    elif func in commands:
        doc = "Manual entry for '{}' is empty".format(func)
        if commands[func].doc:
            doc = "'{}': {}".format(func, commands[func].doc)

    else:
        doc = "No manual entry for '{}'".format(func)
        raise FunctionException(doc)

    await ctx.say(doc)
    return doc

@command()
async def delLastMsg(ctx, *args):
    await ctx.bot.delete_message(ctx.message)
    return 0

@command()
async def ping(ctx, msg, s = False, silent = False):
    """Returns the latency between the Server and the Bot
    Usage: ping"""

    local_time = datetime.now()
    ping_latency = (local_time - ctx.message.timestamp).microseconds // 1000
    if not s and not silent:
        pong = await ctx.say('ping({}ms)'.format(str(ping_latency)))
        pong_latency = (pong.timestamp - local_time).microseconds // 1000
        await ctx.bot.edit_message(pong, '{} pong({}ms)'.format(pong.content, str(pong_latency)))
    return ping_latency

@command()
async def echo(ctx, message: str):
    """Displays text
    Usage: echo <msg:str>"""
    
    message = re.sub("\s+", " ", message.strip())
    await ctx.say(message)
    return message
