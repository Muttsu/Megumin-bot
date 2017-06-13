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

    if message.content.startswith('.'):
        pasecommand(message.content[1:],message)
    elif message.content.startswith('<@!{}>'.format(client.user.id)):
        query = message.content.split()
        result = query.remove('<@!{}>'.format(client.user.id))
        command = ' '.join(result)
        parsecommand(command,message)

def parsecommand(command,message):
    if command == 'ping':
        a = message.timestamp
        b = datetime.now()
        latency = (b - a).microseconds // 1000
        client.send_message(message.channel,'pong - ' + str(latency))
        print('ping')
        
client.run('MzIyMTg2OTkwNTc5NzQ0Nzcy.DCD7VA.yIQEIeyd3QZrhzVVBw6Nguyihx4')
