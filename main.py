import asyncio
import discord

from command import commands
from context import Context

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


bot = discord.Client()


@bot.event
async def on_ready():
    print('Logged in as', bot.user.name, bot.user.id)

    prefix.append('<@{}> '.format(bot.user.id))
    prefix.append('<@!{}> '.format(bot.user.id))


def log(author, state: str, message):
    """Logging Logging Error Debugging"""
    print("[{}] {:<20s}:{:<10s} {}".format(datetime.now().strftime("%H:%M:%S"), str(author), state, str(message)))


async def parse_command(message, command):
    """Parse individual commands"""
    #command.split(" | ")

    cmd = command.split(" ", 2)
    module = cmd[0]
    func_name = cmd[1]
    args = cmd[2:]

    func = commands[func_name].get_func()
    
    tmp = {
        "bot": bot,
        "message": message
    }

    ctx = Context(**tmp)
    del tmp

    if func_name in commands:
        try:
            log(message.author, "SUCCESS", "{}.{} {}".format(module, func_name,
                await func(ctx, *args)))
        except Exception as e:
            log(message.author, "ERROR", command)
            print("  > " + str(e))
            if message.author.id in admin_ids:
                await bot.send_message(message.channel, "Aww")
            else:
                await bot.send_message(message.channel, "Something went wrong and you're the cause. You suck.")
    
    else:
        log(message.author, "ERROR", "{}.{}".format(module, func_name))
        print("  > {}.{} not found.".format(module, func_name))
    

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