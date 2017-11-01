from datetime import datetime
import re

from core import *

@command(ignore_kwargs = True, ignore_carry = True)
async def help(ctx, func: str):
    """Displays the reference manual for commands and aliases
    Usage: help <func:str>"""

    if func in ALIASES:
        doc = "'{}' is an alias for '{}'".format(func, ALIASES[func])

    elif func in COMMANDS:
        doc = "Manual entry for '{}' is empty".format(func)
        if COMMANDS[func].doc:
            doc = "'{}': {}".format(func, COMMANDS[func].doc)

    else:
        doc = "No manual entry for '{}'".format(func)
        raise FunctionException(doc)

    await ctx.reply(doc)
    return doc

@command(ignore_all=True, ignore_ctx=False)
async def delMsg(ctx):
    """Deletes the command message
    Usage: delMsg
    Return: 0"""

    try:
        await ctx.bot.delete_message(ctx.message)
        return 0
    except:
        raise FunctionException()

@command(ignore_all=True, ignore_ctx=False)
async def ping(ctx):
    """Returns the latency between the Server and the Bot
    Usage: ping [-s or -Silent]
    Return: ping"""

    local_time = datetime.now()
    ping_latency = (local_time - ctx.message.timestamp).microseconds // 1000

    pong = await ctx.reply('ping({}ms)'.format(str(ping_latency)))
    if pong is not None:
        pong_latency = (pong.timestamp - local_time).microseconds // 1000
        ret = (await ctx.bot.edit_message(pong, '{} pong({}ms)'.format(pong.content, str(pong_latency)))).content

    return ret

@command(key_aliases = {"f": "formatstr", "r": "raw"})
async def echo(ctx, carry, message="{}", raw = False, formatstr = ""):
    """Displays text [-r or -raw] [-s or -silent] [-formatstr:str]
    Usage: echo <msg:str>"""

    formatstr = carry or formatstr
    message = str(message).format(formatstr)

    if not raw:
        message = re.sub("\s+", " ", message).strip()
    await ctx.reply(message)
    return message

