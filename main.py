import asyncio
import discord

from core import commands
from core import Context

from datetime import datetime
import json
import importlib

print("Strarting BOT...")


with open("config.json", "r") as f:
    secret = json.load(f)
    f.close()


admin_ids = secret["admins"]
prefix = secret["prefix"]
if isinstance(prefix, str):
    prefix = [prefix]
mods = secret["modules"]
modules = {}
for mod in mods:
    modules[mod] = importlib.import_module("modules." + mod)

print("Availiable Commands:")
for c in commands.keys():
    print("  " + c)

bot = discord.Client()


@bot.event
async def on_ready():
    """When the Bot is ready to go"""

    print('Logged in as', bot.user.name, bot.user.id)

    prefix.append('<@{}> '.format(bot.user.id))
    prefix.append('<@!{}> '.format(bot.user.id))


def log(author, state: str, message, info = None):
    """Logging Logging Error Debugging"""
    print("[{}] {:<20s}:{:<10s} {}".format(datetime.now().strftime("%H:%M:%S"), str(author), state, str(message)))
    if message:
        print("  > " + str(info))


async def parse_command(message, command):
    """Parse individual commands"""

    cmd = command.split(" ", 1)
    func_name = cmd[0]
    args = cmd[1:]


    # Check if the command actually exists
    if func_name in commands:
        func = commands[func_name]
        func.ctx = Context(bot = bot, message = message)
        try:
            log(message.author, "SUCCESS", func_name,
                await func(*args))

        # Error parsing
        except Exception as e:
            log(message.author, "ERROR", command, e)

            # So I don't get depressed (◕‿◕✿)
            if message.author.id in admin_ids:
                await bot.send_message(message.channel, "Aww")
            else:
                await bot.send_message(message.channel, "Something went wrong and you're the cause. You suck.")
    else:
        log(message.author, "ERROR", command, "{}: not a command".format(func_name))


async def parse_message(message):
    """Transforms message content into an array of commands"""
    content = message.content
    for pfx in prefix:
        if content.startswith(pfx):
            commands = [*map(lambda string: string.strip(), content.replace(pfx, "", 1).split(" & "))]
            break
    for cmd in commands:
            await parse_command(message, cmd)
    
@bot.event
async def on_message(message):
    if message.channel.name == "megumin-test" and message.author != bot.user: #test only

        if message.content.startswith(tuple(prefix)):
            await parse_message(message)


bot.run(secret["token"])
