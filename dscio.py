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
        if ch in self.pipes:
            self.pipes[ch].write(s)
        else:
            asyncio.ensure_future(self.bot.send_message(ch, s))

    def flush(self):
        del self.stream
        self.stream = {}

class Dscin():
    def __init__(self, bot):
        self.stream = {}
        self.pipes = {}
        self.bot = bot

    async def read(self, n=1):
        #todo raise exception if channel not in self.buffer
        ch = asyncio.Task.current_task().ctx.invoker.channel #only allows current channel
        q = self.stream[ch]
        ret = [await q.get() for i in range(n)]
        return ret


    def write(self, s, channel=asyncio.Task.current_task().ctx.invoker.channel):
        #todo raise exception if channel not in self.buffer
        asyncio.ensure_future(self.stream[channel].put(Dummy_msg(s, channel)))

    def new_buffer(self, channel=asyncio.Task.current_task().ctx.invoker.channel):
        #todo raise exception if channel in self.buffer
        q = asyncio.Queue()
        self.stream[channel] = q

    def close_buffer(self, channel=asyncio.Task.current_task().ctx.invoker.channel):
        del self.stream[channel]


class Dummy_msg():
    def __init__(self, content, channel = asyncio.Task.current_task().ctx.invoker.channel):
        self.channel = channel
        self.content = content