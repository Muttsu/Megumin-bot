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

async def ping_check(message):
    a = message.timestamp
    b = datetime.now()
    latency = (b - a).microseconds // 1000
    pong = await bot.send_message(message.channel, 'pong    {0}ms'.format(str(latency)))
    c = pong.timestamp
    latency2 = (c - b).microseconds // 1000
    await bot.edit_message(pong,pong.content+'    ping    {0}ms'.format(str(latency2)))
    print('ping from {0}    {1}    {2}    ms'.format(str(message.author), str(latency), str(latency2)))

@bot.command(pass_context = True)
async def ping(ctx):
    await ping_check(ctx.message)

@bot.listen()
async def on_message(message):
    if message.content == 'ping':
        await ping_check(message)

        
bot.run('MzIyMTg2OTkwNTc5NzQ0Nzcy.DCD7VA.yIQEIeyd3QZrhzVVBw6Nguyihx4')
