import discord
from discord.ext import commands
import asyncio
from datetime import datetime

bot = commands.Bot(command_prefix = '?')

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    bot.command_prefix = ['?','<@!{0}> '.format(bot.user.id)]
    print(':3')

@bot.command(pass_context = True)
async def ping(ctx):
    a = ctx.message.timestamp
    b = datetime.now()
    latency = (b - a).microseconds // 1000
    await bot.say('pong    {0}'.format(str(latency)))
    print('ping from {0}: {1}'.format(ctx.message.author, str(latency)))

@bot.listen()
async def on_message(message):
    if message.content == 'ping':
        a = message.timestamp
        b = datetime.now()
        latency = (b - a).microseconds // 1000
        pong = await bot.send_message(message.channel, 'pong    {0}ms'.format(str(latency)))
        c = pong.timestamp
        latency2 = (c - b).microseconds // 1000
        ping = await bot.edit_message(pong,pong.content+'    ping    {0}ms'.format(str(latency2)))

        
bot.run('MzIyMTg2OTkwNTc5NzQ0Nzcy.DCD7VA.yIQEIeyd3QZrhzVVBw6Nguyihx4')
