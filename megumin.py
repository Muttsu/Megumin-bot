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
    if client.user in message.mention and 'ping' in message.content:
        ping = message.timestamp
        pong = datetime.now()
        latency = (pong - ping).microseconds // 1000
        await client.send_message(message.channel,'pong - ' + str(latency))
        print('ping')
        
client.run('MzIyMTg2OTkwNTc5NzQ0Nzcy.DCD7VA.yIQEIeyd3QZrhzVVBw6Nguyihx4')
