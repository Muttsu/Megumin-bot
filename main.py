import discord

from core import *

from datetime import datetime
import json
import importlib


ready = Start("BOT")


bot = discord.Client()

token = secret["token"]

admin_ids = secret["admins"]
importlib.import_module("core").admin_ids = admin_ids

prefix = secret["prefix"]
modules = secret["modules"]
if "aliases" in secret:
    # wa ga nawa megumin! EXPLOSION (it was super effective!) ಠ_ಠ
    aliases = secret["aliases"]
    importlib.import_module("core").aliases = aliases


for mod in modules:
    importlib.import_module("modules." + mod)
print("Availiable Commands: {}".format(sorted(tuple(commands.keys()) + tuple(aliases.keys()))))


@bot.event
async def on_ready():
    """Are you ready?"""

    log(bot.user, "Logged in as " + bot.user.id)
    print("-"*63)

    # Prefix Stuff
    if isinstance(prefix, str):
        bot.prefix = [prefix]
    else:
        bot.prefix = [*prefix]
    # Support for @mentions
    bot.prefix.append('<@{}> '.format(bot.user.id))
    bot.prefix.append('<@!{}> '.format(bot.user.id))

    ready()


@bot.event
async def on_message(message):
    """Commands and Stuff"""

    if ready:
        if message.author != bot.user:
            if message.content == "§die" and message.author.id in admin_ids:
                exit()
            if message.content.startswith(tuple(bot.prefix)):
                log(message.author, message.content)
                ctx = Context(bot = bot, message = message)
                await parse_message(ctx)
                print("-"*3)


bot.run(token)
