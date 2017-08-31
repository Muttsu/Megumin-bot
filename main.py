import discord

from core import *

from datetime import datetime
import json
import importlib


ready = Start("BOT")


bot = discord.Client()

token = secret["token"]
admin_ids = secret["admins"]
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
                await parse_message(message)
                print("-"*3)

#################################
# == There is NOTHING To See == #
#################################

async def parse_message(message):
    """Removes Prefixes and Passes the Command to parse_command()"""

    content = message.content
    for pfx in bot.prefix:
        if content.startswith(pfx):
            # Remove prefix from message 
            command = content.replace(pfx, "", 1).strip()
            break
            
    try:
        await parse_command(message, command)

    # Error parsing (◕‿◕✿)
    except FunctionException as e:
        log(message.author, "FUNCTION EXPLODED", content, e)
        await bot.send_message(message.channel,
            "Kazuma, Kazuma. Is this normal?```\n> {}\n```".format(str(e)))

    except Exception as e:
        log(message.author, "ERROR", content, e)
        await bot.send_message(message.channel,
            "This is NOT how it works. ಠ_ಠ```\n> {}```".format(str(e)))

        # So I don't get depressed (◕‿◕✿)
        #if message.author.id in admin_ids:
        #    await bot.send_message(message.channel, "Aww")
        #else:
        #    await bot.send_message(message.channel, "Something went wrong and you're the cause. You suck.")


async def parse_command(message, command, carry = None):
    """Parse commands"""
    
    stack = []
    cmds = command.split(" & ")
    
    for cmd in cmds:
        car = Start(carry)
        cmd = cmd.split(" | ")
        for c in cmd:
            r = await execute(message, c, stack, car)
            stack.append(r)
            car()
    return r


async def execute(message, command, stack, carry = False):
    command = command.strip()
    func_name = command.split(" ", 1)[0]
    arg = command.replace(func_name, "", 1).strip()

    if func_name in aliases:
        return await parse_command(message, "{} {}".format(parse_alias(func_name), arg), carry)
    
    # Check if the command actually exists
    elif func_name in commands:
        func = commands[func_name]
        # Smartz way to pass bot and message objects
        func.ctx = Context(bot = bot, message = message)
        
        if carry:
            arg = str(stack.pop())
    
        r = await func(arg)
        
        # Log the return value
        log(message.author, "SUCCESS", command, r)
        return r

    else:
        raise Exception("'{}': not a command".format(func_name))


def parse_alias(func_name):
    # Alias of an Alias
    if func_name in aliases:
        return parse_alias(aliases[func_name])
    # We found the Function (maybe?)
    else:
        return func_name



def log(author, state: str, message = "", info = None):
    """Logging, Logging, Error Debugging"""
    print("[{}] {:<20s}:{:<20s} {}".format(datetime.now().strftime("%H:%M:%S"), str(author), state, str(message)))
    if info:
        print("  > " + str(info))



bot.run(token)
