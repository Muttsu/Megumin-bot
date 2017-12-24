"""io flow for discord messages"""
import asyncio

class Dscout(): #flow control
    def __init__(self, bot, pipes = {}):
        self.pipes = pipes
        self.bot = bot

    def write(self,s):
        s = s.strip()
        if not s:
            return #need to implement exception
        ch = asyncio.Task.current_task().ctx.invoker.channel
        if self.pipes and self.pipes[ch]:
            self.pipes[ch].write(s)
        else:
            asyncio.ensure_future(self.bot.send_message(ch, s))

    def flush(self):
        del self.stream
        self.stream = {}

class Dscin():
    def __init__(self, bot):
        self.buffer = []
        self.pipes = {}
        self.bot = bot
        self.lock = asyncio.Semaphore(0)

    async def read(self, n=1, channel=asyncio.Task.current_task().ctx.invoker.channel):
        while await self.lock.acquire():
            for msg in self.buffer:
                if msg.channel = channel:
                    

    def write(self, s):
        self.buffer.append(Dummy_msg(s))
        self.lock.release()


class Dummy_msg():
    def __init__(self, content, channel = asyncio.Task.current_task().ctx.invoker.channel):
        self.channel = channel
        self.content = content