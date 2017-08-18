import discord
from discord.ext import commands
import asyncio

import re
from datetime import datetime
import json

with open("config.json". "r") as f:
    secret = json.load(f)
    f.close()

print("Strarting BOT...")
bot = commands.Bot("!")

admins = secret["admins"]

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)

    prefix = [bot.command_prefix]
    prefix.append('<@{}> '.format(bot.user.id))
    prefix.append('<@!{}> '.format(bot.user.id))
    bot.command_prefix = prefix


# Ping {{{

async def ping_check(message):
    ping = message
    local_time = datetime.now()
    ping_latency = (local_time - ping.timestamp).microseconds // 1000
    pong = await bot.send_message(message.channel, 'ping({}ms)'.format(str(ping_latency)))
    pong_latency = (pong.timestamp - local_time).microseconds // 1000
    await bot.edit_message(pong,'{} pong({}ms)'.format(pong.content, str(pong_latency)))

    log(str(message.author), "Ping", "({}ms) ({}ms)".format(ping_latency, pong_latency))

# }}}
# Spam Function {{{

async def spam_function(message):
    async def log_error(error):
        await bot.edit_message(header,
            "```\n-- Spam Function Error:[{}] --\n```".format(error))

    header = await bot.send_message(message.channel, "```\n-- Spam Function Active --\n```")
    args = message.content.split()
    if len(args) < 3:
        await log_error("2 arguments required")
    else:
        if(message.channel.name != "megumin-test"):
            await bot.delete_message(message)
        
        tmp = []
        content = " ".join(args[2:])
        reps = int(args[1]) or 3
        
        log(str(message.author), "Spam", "[{}, \"{}\"]".format(reps, content))
        
        for _ in range(reps):
            tmp.append(await bot.send_message(message.channel, "{} - spam {}".format(content, _ + 1)))
        for msg in tmp[::-1]:
            await bot.delete_message(msg)
        await bot.delete_message(header)
        
@bot.command(pass_context=True)
async def spam(ctx, count : int, *, content):
    log(str(ctx.message.author), "Spam", "[{}, \"{}\"]".format(count, content))

    if(ctx.message.channel.name != "megumin-test"):
        await bot.delete_message(ctx.message)

    async def editCount(index):
        await bot.edit_message(header,
            "```\n-- Spam Function Active [{}] --\n```".format(index))

    header = await bot.say("```\n-- Spam Function Active --\n```")
    await bot.say(content)
    for _ in range(count):
        await bot.delete_message(await bot.say(content))
        await editCount(_+1)
    await bot.delete_message(header)

# }}}
# Explosion {{{

async def explosion_function(message):
    if message.channel.name != "megumin-test":
        await bot.delete_message(message)

    author = message.author

    arguments = re.sub("\S+\s+", "", message.content, 1)

    members_id = [*map(lambda s: re.search("\d+", s).group(0),
        re.search("^(<@!?\d+>\s*)+", arguments).group(0).split())]
    members = [*filter(lambda m: m.id in members_id,
        bot.get_all_members())]
    members_name = [*map(lambda m: m.name, members)]

    args = re.sub("^(<@!?\d+>\s*)+", "", arguments) or "3 EXPLOSION"

    try:
        count = int(re.search("^\d+", args).group(0))
    except:
        count = 3
    content = re.sub("^\d+\s*", "", args, 1) or "EXPLOSION"

    log(str(author), "Explosion", "[{}, {}, \"{}\"]".format(members_name, count, content))

    for m in members:
        for _ in range(count):
            await bot.send_message(m, content)


@bot.command(pass_context=True)
async def explosion(ctx, id, count=3, *, content="EXPLOSION"):
    if ctx.message.channel.name != "megumin-test":
        await bot.delete_message(ctx.message)

    member = discord.utils.get(bot.get_all_members(), id=re.sub("\D+", "", id))
    author = ctx.message.author

    log(str(author), "Explosion", "[{}, {}, \"{}\"]".format(member, count, content))

    if(ctx.message.channel.name != "megumin-test"):
        await bot.delete_message(ctx.message)

    for _ in range(count):
        await bot.send_message(member, "<@{}>: {}".format(author.id, content))
            
# }}}

async def msg_function(message):
    arguments = re.sub("^\w+", "", message.content, 1).strip()
    author = message.author
    receiver = discord.utils.get(bot.get_all_members(), id=re.search("^<@!{0,1}(\d+)>", arguments).group(1))
    content = re.sub("^<@!{0,1}\d+>", "",arguments, 1).strip()

    log(str(author), "Message", "[{}, \"{}\"]".format(receiver, content))
    
    await bot.send_message(receiver, "<@{}>: {}".format(author.id, content))

def log(author: str, function: str, arguments: str):
    print("{:>20}: {:<10} {}".format(author, function, arguments))

@bot.listen()
async def on_message(message):
    if message.author.id in admins:
        if message.content == 'ping':
            await ping_check(message)

        elif message.content.startswith('spam '):
            await spam_function(message)

        elif message.content.startswith('explosion '):
            await explosion_function(message)

        elif message.content.startswith('msg '):
            await msg_function(message)

        elif message.content == "§die":
            exit()

bot.run(secret["token"])
