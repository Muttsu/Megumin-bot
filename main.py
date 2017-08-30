import asyncio
import discord

from core import *

from datetime import datetime
import json
import importlib


ready = Start()

bot = discord.Client()


token = secret["token"]
admin_ids = secret["admins"]
prefix = secret["prefix"]
modules = secret["modules"]
for mod in modules:
    importlib.import_module("modules." + mod)
print("Availiable Commands: {}".format(tuple(sorted(commands.keys()))))



@bot.event
async def on_ready():
    """Are you ready?"""

    log(bot.user, "Logged in as", bot.user.id)
    print("-"*63)

    ready()

    # Prefix Stuff
    if isinstance(prefix, str):
        bot.prefix = [prefix]
    else:
        bot.prefix = [*prefix]
    # Support for @mentions
    bot.prefix.append('<@{}> '.format(bot.user.id))
    bot.prefix.append('<@!{}> '.format(bot.user.id))


@bot.event
async def on_message(message):
    """Commands and Stuff"""

    if ready:
        # Test Only
        if message.channel.name == "megumin-test" and message.author != bot.user:
            if message.content == "§die":
                exit()
            if message.content.startswith(tuple(prefix)):
                await parse_message(bot, message)


bot.run(token)
