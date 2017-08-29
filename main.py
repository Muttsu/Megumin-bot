import asyncio
import discord

from core import commands, Context

from datetime import datetime
import json
import importlib

print("Strarting BOT...")

bot = discord.Client()


# Data from Config File
with open("config.json", "r") as f:
    secret = json.load(f)
    f.close()

token = secret["token"]
admin_ids = secret["admins"]
prefix = secret["prefix"]
modules = secret["modules"]


@bot.event
async def on_message(message):
    """Commands and Stuff"""

    # Test Only
    if message.channel.name == "megumin-test" and message.author != bot.user:

        if message.content.startswith(tuple(prefix)):
            await parse_message(message)


@bot.event
async def on_ready():
    """Are you ready?"""

    print('Logged in as', bot.user.name, bot.user.id)

    # Prefix Stuff
    if isinstance(prefix, str):
        bot.prefix = [prefix]
    else:
        bot.prefix = [*prefix]
    # Support for @mentions
    bot.prefix.append('<@{}> '.format(bot.user.id))
    bot.prefix.append('<@!{}> '.format(bot.user.id))


##################################
# == Thats All You Need To Know ==
##################################


async def parse_message(message):
    """Transforms message content into an array of commands"""

    content = message.content
    for pfx in bot.prefix:
        if content.startswith(pfx):
            # Remove prefix from message
            commands = map(lambda string: string.strip(),
                # Split the commands
                content.replace(pfx, "", 1).split(" & "))
            break

    for cmd in commands:
            await parse_command(message, cmd)


async def parse_command(message, command):
    """Parse individual commands"""

    cmd = command.split(" ", 1)
    func_name = cmd[0]
    args = cmd[1:]


    # Check if the command actually exists
    if func_name in commands:
        func = commands[func_name]
        # Smartz way to pass bot and message objects
        func.ctx = Context(bot = bot, message = message)
        try:
            # Log the return value
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

def log(author, state: str, message = None, info = None):
    """Logging, Logging, Error Debugging"""
    print("[{}] {:<20s}:{:<10s} {}".format(datetime.now().strftime("%H:%M:%S"), str(author), state, str(message)))
    if message:
        print("  > " + str(info))


for mod in modules:
    importlib.import_module("modules." + mod)
print("Availiable Commands: {}".format(tuple(commands.keys())))

bot.run(token)
