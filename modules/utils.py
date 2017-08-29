import asyncio
from datetime import datetime

from core import command

@command()
async def ping(ctx, *args):
    local_time = datetime.now()
    ping_latency = (local_time - ctx.message.timestamp).microseconds // 1000
    pong = await ctx.say('ping({}ms)'.format(str(ping_latency)))
    pong_latency = (pong.timestamp - local_time).microseconds // 1000
    await ctx.bot.edit_message(pong, '{} pong({}ms)'.format(pong.content, str(pong_latency)))
    return ping_latency

@command()
async def echo(ctx, message):
    await ctx.say(message)
    return message

