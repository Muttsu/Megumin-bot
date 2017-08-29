import discord
import sys
import inspect
from discord.ext import commands
import asyncio

import re
from datetime import datetime
import json


print("Strarting BOT...")


with open("config.json", "r") as f:
    secret = json.load(f)
    f.close()


admin_ids = secret["admins"]
prefix = secret["prefix"]
modules = secret["modules"]

mods = {}
for module in modules:
    mods[module] = importlib.import_module(module)

bot = commands.Bot(prefix)


@bot.event
async def on_ready():
    print('Logged in as', bot.user.name, bot.user.id)

    prefix = [bot.command_prefix]
    prefix.append('<@{}> '.format(bot.user.id))
    prefix.append('<@!{}> '.format(bot.user.id))
    bot.command_prefix = prefix


@bot.event
async def on_message(message):
    if message.author.id in admin_ids and message.channel.name == "megumin-test": #test only

        def parse_command(message):
            cmd = message.content.split(' ', 2)
            mod = cmd[0]
            fct = cmd[1]
            args = # some regex and stuff
            getattr(mods[mod],fct)(message, args)

        if message.content.startswith(tuple(bot.command_prefix)):
            for pfx in bot.command_prefix:
                message.content.replace(pfx,'').strip()
            if ' & ' in message.content:
                cmds = message.content.split(' & ')
                for cmd in cmds:
                    message.content = cmd
                    parse_command(message)
            else:
                parse_command(message)


bot.run(secret["token"])