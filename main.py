import discord
import sys
import inspect
from discord.ext import commands
import asyncio
import core

import re
from datetime import datetime
import json
import importlib

print("Strarting BOT...")


with open("config.json", "r") as f:
    secret = json.load(f)
    f.close()


admin_ids = secret["admins"]
prefix = secret["prefix"]
mods = secret["modules"]

modules = {}
for mod in mods:
    modules[mod] = importlib.import_module("modules." + mod)

bot = commands.Bot(prefix)


@bot.event
async def on_ready():
    print('Logged in as', bot.user.name, bot.user.id)

    if isinstance(bot.command_prefix, str):
        prefix = [bot.command_prefix]
    prefix.append('<@{}> '.format(bot.user.id))
    prefix.append('<@!{}> '.format(bot.user.id))
    bot.command_prefix = prefix


def log(author, state: str, message):
    """Logging Logging Error Debugging"""
    print("[{}] {:<20s}:{:<10s} {}".format(datetime.now().strftime("%H:%M:%S"), str(author), state, str(message)))


async def parse_command(message, command):
    """Parse individual commands"""
    #command.split(" | ")

    try:
        cmd = command.split(" ", 2)
        module = cmd[0]
        func_name = cmd[1]
        args = cmd[2:]
        func = getattr(modules[module], func_name)
    except:
        cmd = command.split(" ", 1)
        module = "core"
        func_name = cmd[0]
        args = cmd[1:]
        func = getattr(core, func_name)

    try:
        log(message.author, "SUCCESS", "{}.{} {}".format(module, func_name,
            await func(*args, bot = bot, message = message)))
    except Exception as e:
        log(message.author, "ERROR", command)
        print("  > " + str(e))
        if message.author.id in admin_ids:
            await bot.send_message(message.channel, "Aww")
        else:
            await bot.send_message(message.channel, "Something went wrong and you're the cause. You suck.")
    

async def parse_message(message):
    """Transforms message content into an array of commands"""
    content = message.content
    for pfx in bot.command_prefix:
        if content.startswith(pfx):
            commands = [*map(lambda string: string.strip(), content.replace(pfx, "", 1).split(" & "))]
            break
    for cmd in commands:
            await parse_command(message, cmd)
    
@bot.event
async def on_message(message):
    if message.channel.name == "megumin-test" and message.author != bot.user: #test only

        if message.content.startswith(tuple(bot.command_prefix)):
            await parse_message(message)


bot.run(secret["token"])