"""File to run"""
import importlib, asyncio
from core import Start, log, get_task, parse_message
from bot import bot
from dscio import dscin, dscout

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

            # todo write task factory instead of
            task = get_task()
            task.author = message.author
            task.channel = message.channel
            task.invoker = message
            del task

            if dscin.flag.is_set():
                dscin.put(message, message.channel)
            else:
                await parse_message({}) # todo write new invoke function


bot.init()
