"""File to run"""
import importlib, asyncio
from core import * # pylint: disable=W0614,W0401

ready = Start("BOT") # pylint: disable=C0103


# == Import custom modules ==
for mod in bot.modules:
    importlib.import_module("modules." + mod)

print("Availiable Commands: {}".format(sorted(tuple(bot.commands.keys()) + tuple(bot.aliases.keys()))))


@bot.event
async def on_ready():
    """Are you ready?"""

    log(bot.user, "Logged in as " + bot.user.id)
    print("-"*63)

    # Prefix Stuff
    bot.command_prefix.append('<@{}> '.format(bot.user.id))
    bot.command_prefix.append('<@!{}> '.format(bot.user.id))

    ready()


@bot.event
async def on_message(message):
    """Commands and Stuff"""

    if ready and message.author != bot.user:
        if message.content == "§die" and message.author.id in bot.admin_ids:
            asyncio.get_event_loop().stop()

        elif message.content.startswith(tuple(bot.command_prefix)):
            log(message.author, message.content)

            #!!! add new bot class with active context
            ctx = Context(bot=bot, message=message)

            await parse_message(ctx)
            print("-"*3)




bot.init()
