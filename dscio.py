"""io flow for discord messages"""
import asyncio, discord
from bot import bot

class Dscout():
    """unbuffered output stream
    enables channel redirrection using a dict mapping"""
    def __init__(self, client):
        self.pipes = {}
        self.client = client

    def write(self, s, channel=None):
        if channel is None: channel = asyncio.Task.current_task().channel
        s = s.strip()
        if not s:
            return # what are you returning???
            # need to implement exception
        if channel in self.pipes:
            self.pipes[channel].write(s)
        else:
            asyncio.ensure_future(self.client.send_message(channel, s))

    def new_pipe(self, from_ch, to_ch):
        self.pipes[from_ch] = to_ch

    def del_pipe(self, from_ch):
        del self.pipes[from_ch]

    def del_pipe_to(self, to_ch):
        for k, v in self.pipes:
            if v == to_ch:
                del self.pipes[k]


    def flush(self):
        return # flush is not allowed
        # todo implement multiple prints / single message; use flush to end further printing


class Dscin():
    """buffered input stream
    enables channel redirrection using a dict mapping"""
    def __init__(self):
        self.stream = {}
        self.pipes = {}
        self.flag = asyncio.Event()

    async def get(self, channel=None):
        if channel is None:
            channel = asyncio.Task.current_task().channel
        # todo raise exception if channel not in self.buffer
        # todo read n times
        if self.stream and channel in self.stream:
            buf = self.stream[channel]
            ret = await buf.get()
            if buf.isempty():
                self.close_buffer(channel)
        else:
            self.new_buffer(channel)
            ret = self.get()
        return ret

    async def read(self, **kwargs):
        return await self.get(**kwargs).content


    def put(self, element, channel=None):
        if channel is None:
            channel = asyncio.Task.current_task().channel
        # todo raise exception if channel not in self.buffer
        # todo pipes
        if self.stream and channel in self.pipes:
            self.pipes[channel].put(element)
        else:
            if channel not in self.stream:
                self.new_buffer(channel)
            self.stream[channel].put(element)

    def write(self, s, **kwargs):
        self.put(dummy_msg(s), **kwargs)


    def new_buffer(self, channel=None):
        if channel is None:
            channel = asyncio.Task.current_task().channel
        # todo raise exception if channel in self.buffer
        self.stream[channel] = buffer()

    def close_buffer(self, channel=None):
        if channel is None:
            channel = asyncio.Task.current_task().channel
        del self.stream[channel]

    def new_pipe(self, from_ch, to_ch):
        self.pipes[from_ch] = to_ch

    def del_pipe(self, from_ch):
        del self.pipes[from_ch]

    def del_pipe_to(self, to_ch):
        for k, v in self.pipes:
            if v == to_ch:
                del self.pipes[k]

class buffer():
    """underlaying buffer for dscin.
    The buffer uses a fifo queue to store elements.
    there is also a lock to block and intercept the queue
    using context manager statement"""

    def __init__(self, *, loop=asyncio.get_event_loop()):
        self._lock = asyncio.Lock()
        self._cargo = asyncio.Queue()
        self._loop = loop
        self.size = 0


    async def get(self):
        with await self._lock:
            self.size -= 1
            return await self._cargo.get()

    async def read(self):
        return await self.get().content


    def put(self, message):
        self._cargo.put_nowait(message)
        self.size += 1

    def write(self, s):
        self.put(dummy_msg(s))


    def isempty(self):
        return self.size == 0

    async def _acquire(self):
        if not self._lock._locked and all(w.cancelled() for w in self._lock._waiters):
            self._lock._locked = True
            return self._cargo

        fut = self._lock._loop.create_future()
        self._lock._waiters.appendleft(fut)
        try:
            await fut
            self._lock._locked = True
            return self._cargo
        except asyncio.futures.CancelledError:
            if not self._lock._locked:
                self._lock._wake_up_first()
            raise
        finally:
            self._lock._waiters.remove(fut)

    def _release(self):
        self._lock.release()


    async def __aenter__(self):
        return self._acquire()

    async def __aexit__(self, exc_type, exc, tb):
        self._release()


    def flush(self):
        del self._cargo
        self._cargo = asyncio.Queue()


class dummy_msg():
    def __init__(self, content):
        self.reactions = []
        self.edited_timestamp = None
        self.timestamp = None
        self.tts = False
        self.pinned = False
        self.content = content
        self.mention_everyone = None
        self.embeds = None
        self.id = None
        self.channel = None
        self.author = {}
        self.nonce = None
        self.attachments = None
        self.type = None
        self.server = None
        self.channel = None
        self.mentions = []
        self.channel_mentions = []
        self.role_mentions = []
        self.call = None

dscin = Dscin()
dscout = Dscout(bot)

