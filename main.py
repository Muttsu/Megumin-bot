"""File to run"""
import importlib
from core import * # pylint: disable=W0614,W0401


ready = Start("BOT") # pylint: disable=C0103


# == Import custom modules ==
for mod in MODULES:
    importlib.import_module("modules." + mod)

print("Availiable Commands: {}".format(sorted(tuple(COMMANDS.keys()) + tuple(ALIASES.keys()))))


@bot.event
async def on_ready():
    """Are you ready?"""

    log(bot.user, "Logged in as " + bot.user.id)
    print("-"*63)

    # Prefix Stuff
    PREFIX.append('<@{}> '.format(bot.user.id))
    PREFIX.append('<@!{}> '.format(bot.user.id))

    ready()


@bot.event
async def on_message(message):
    """Commands and Stuff"""

    if ready:
        if message.author != bot.user:
            if message.content == "§die" and message.author.id in ADMIN_IDS:
                exit()

            elif message.content.startswith("§commands_enabled"):
                string = message.content.replace("§commands_enabled", "", 1).strip()
                if re.match("f", string):
                    bot.commands_enabled = False
                elif re.match("t", string):
                    bot.commands_enabled = True
                if bot.commands_enabled:
                    log(message.author, "Commands Enabled")
                else:
                    log(message.author, "Commands Disabled")

            elif message.content.startswith(tuple(PREFIX)):
                log(message.author, message.content)

                #!!! add new bot class with active context
                ctx = Context(bot=bot, message=message)
                
                await parse_message(ctx)
                print("-"*3)


bot.run(TOKEN)
