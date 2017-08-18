import discord
from discord.ext import commands
import asyncio

import re
from datetime import datetime

bot = commands.Bot(command_prefix='?')


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    bot.command_prefix = ['?',
        '<@!{}> '.format(bot.user.id),
        '<@{}> '.format(bot.user.id)]


# Ping {{{

async def ping_check(message):
    ping = message
    local_time = datetime.now()
    ping_latency = (local_time - ping.timestamp).microseconds // 1000
    pong = await bot.send_message(message.channel, 'ping({}ms)'.format(str(ping_latency)))
    pong_latency = (pong.timestamp - local_time).microseconds // 1000
    await bot.edit_message(pong,'{} pong({}ms)'.format(pong.content, str(pong_latency)))
    print('{}: ping({}ms) pong({}ms)'.format(message.author, ping_latency, pong_latency))

# }}}
# Spam Function {{{

async def spam_function(message):
    async def log_error(error):
        await bot.edit_message(header,
            """```
-- Spam Function Error:[{}] --
```""".format(error))

    header = await bot.send_message(message.channel, "```\n-- Spam Function Active --\n```")
    args = message.content.split()
    if len(args) < 3:
        await log_error("2 arguments required")
    else:
        await bot.delete_message(message)
        tmp = []
        reps = int(args[1]) or 3
        for _ in range(reps):
            tmp.append(await bot.send_message(message.channel, "{} - spam {}".format(" ".join(args[2:]), _ + 1)))
        for msg in tmp[::-1]:
            await bot.delete_message(msg)
        await bot.delete_message(header)

# }}}

@bot.command(pass_context=True)
async def spam(ctx, count : int, *, content):
    print("{}: Spam [{}, \"{}\"]".format(ctx.message.author, count, content))

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
    
@bot.command(pass_context=True)
async def explosion(ctx, id, count=3, *, content="EXPLOSION"):
    print("{}: explosion [{}, {}, \"{}\"]".format(ctx.message.author, member.name, count, content))

    if(ctx.message.channel.name != "megumin-test"):
        await bot.delete_message(ctx.message)

    author = ctx.message.author
    member = discord.utils.get(bot.get_all_members(), id=re.sub("\D+", "", id))
    for _ in range(count):
        await bot.send_message(member, "<@!{}> -> <@!{}>: {}".format(author.id, member.id, content))

@bot.listen()
async def on_message(message):
    if message.content == 'ping':
        await ping_check(message)
    elif message.content.startswith('spam '):
        await spam_function(message)
    elif message.content == "§die":
        exit()

bot.run('MzIyMTg2OTkwNTc5NzQ0Nzcy.DCD7VA.yIQEIeyd3QZrhzVVBw6Nguyihx4')
