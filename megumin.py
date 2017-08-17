import discord
from discord.ext import commands
import asyncio
from datetime import datetime

bot = commands.Bot(command_prefix='?')


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    bot.command_prefix = ['?',
                          '<@!{0}> '.format(bot.user.id),
                          '<@{0}> '.format(bot.user.id)]


# Ping {{{

async def ping_check(message):
    ping = message
    local_time = datetime.now()
    ping_latency = (local_time - ping.timestamp).microseconds // 1000
    pong = await bot.send_message(message.channel, 'ping({0}ms)'.format(str(ping_latency)))
    pong_latency = (pong.timestamp - local_time).microseconds // 1000
    await bot.edit_message(pong,'{0}    pong({1}ms)'.format(pong.content, str(pong_latency)))
    print('ping from {0}    {1}    {2}    ms'.format(str(message.author), str(ping_latency), str(pong_latency)))


@bot.command(pass_context=True)
async def ping(ctx):
    await ping_check(ctx.message)


@bot.listen()
async def on_message(message):
    if message.content == 'ping':
        await ping_check(message)

# }}}

bot.run('MzIyMTg2OTkwNTc5NzQ0Nzcy.DCD7VA.yIQEIeyd3QZrhzVVBw6Nguyihx4')
