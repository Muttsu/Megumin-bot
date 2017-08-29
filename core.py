import discord
import asyncio
import functools
from datetime import datetime

def def_command(fn):
    @functools.wraps(fn)
    async def func_wrapper(*args, bot, message, **kargs):
        fn.__globals__["bot"] = bot
        fn.__globals__["message"] = message
        return await fn(*args, **kargs)
    return func_wrapper


@def_command
async def ping():
    local_time = datetime.now()
    ping_latency = (local_time - message.timestamp).microseconds // 1000
    pong = await bot.send_message(message.channel, 'ping({}ms)'.format(str(ping_latency)))
    pong_latency = (pong.timestamp - local_time).microseconds // 1000
    await bot.edit_message(pong, '{} pong({}ms)'.format(pong.content, str(pong_latency)))
    return ping_latency

@def_command
async def echo(msg):
    await bot.send_message(message.channel, msg)
    return msg
