import discord
from discord.ext import commands
import asyncio
from datetime import datetime

bot = commands.Bot()

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    bot.command_prefix = ['?','<@!{0}'.format(bot.user.id)]
    print(':3')

@bot.command()
async def ping():
    a = message.timestamp
    b = datetime.now()
    latency = (b - a).microseconds // 1000
    bot.send_message(message.channel,'pong - ' + str(latency))
    print('ping')
        
bot.run('MzIyMTg2OTkwNTc5NzQ0Nzcy.DCD7VA.yIQEIeyd3QZrhzVVBw6Nguyihx4')
