import discord
import asyncio
from datetime import datetime

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print(':3')
    
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    else:
        print(message.content)

    if client.user in message.mentions:
        query = message.content.split()
        command = filter(lambda x : x != '<@{}>'.format(client.user.id) , query)
    elif message.content.startswith('.'):
        command = message.content[1:].split()
    else:
        command = None

    if command != None:
        #parsecommand(command)
        if command[0] == 'ping':
            ping = message.timestamp
            pong = datetime.now()
            latency = (pong - ping).microseconds // 1000
            await client.send_message(message.channel,'pong - ' + str(latency))
            print('ping')
        
client.run('MzIyMTg2OTkwNTc5NzQ0Nzcy.DCD7VA.yIQEIeyd3QZrhzVVBw6Nguyihx4')
