import discord
import asyncio
from datetime import datetime

from command import command


@command()
async def ping(ctx, *args):
    local_time = datetime.now()
    ping_latency = (local_time - ctx.message.timestamp).microseconds // 1000
    pong = await ctx.bot.send_message(ctx.message.channel, 'ping({}ms)'.format(str(ping_latency)))
    pong_latency = (pong.timestamp - local_time).microseconds // 1000
    await ctx.bot.edit_message(pong, '{} pong({}ms)'.format(pong.content, str(pong_latency)))
    return ping_latency

@command()
async def echo(ctx, args):
    await ctx.bot.send_message(ctx.message.channel, args)
    return args

@command()
async def test(ctx):
    bot.sent_message(ctx.message.channel, ctx.message.conent)
