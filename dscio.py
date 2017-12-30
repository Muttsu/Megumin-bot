"""io flow for discord messages"""
import asyncio

class Dscout():
    """unbuffered output stream
    enables channel redirrection using a dict mapping"""
    def __init__(self, bot, pipes={}):
        self.pipes = pipes
        self.bot = bot

    def write(self, s):
        s = s.strip()
        if not s:
            return # what are you returning???
            # need to implement exception
        ch = asyncio.Task.current_task().ctx.invoker.channel
        if ch in self.pipes:
            self.pipes[ch].write(s)
        else:
            asyncio.ensure_future(self.bot.send_message(ch, s))

    def flush(self)
        raise #flush is not allowed


class Dscin(metaclass=Singleton):
    """buffered input stream
    enables channel redirrection using a dict mapping"""
    def __init__(self, bot, pipes={}):
        self._stream = {}
        self.bot = bot
        self.pipes = pipes

    async def read(self, n=1):
        # todo raise exception if channel not in self.buffer
        ch = asyncio.Task.current_task().ctx.invoker.channel
        # only allows current channel
        for i, msg in enumerate(stream)

    def write(self, s, channel=asyncio.Task.current_task().ctx.invoker.channel):
        # todo raise exception if channel not in self.buffer
        asyncio.ensure_future(self.stream[channel].put(Dummy_msg(s, channel)))

    def new_buffer(self, channel=asyncio.Task.current_task().ctx.invoker.channel):
        # todo raise exception if channel in self.buffer
        q = asyncio.Queue()
        self.stream[channel] = q

    def close_buffer(self, channel=asyncio.Task.current_task().ctx.invoker.channel):
        del self.stream[channel]

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
            size += 1
            return await self._cargo.get()


    def put(self, element):
        self._cargo.put_nowait(element)
        size -= 1


    async def _acquire(self):
        if not self._lock._locked and all(w.cancelled() for w in self._lock._waiters):
            self._lock._locked = True
            return self._cargo

        fut = self._lock._loop.create_future()
        self._lock._waiters.appendleft(fut)
        try:
            yield from fut
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

    async def __aexit__(self):
        self._release()


    def flush():
        del self._cargo
        self._cargo = collections.deque()


class dummy_msg():
    def __init__(self, content, channel=asyncio.Task.current_task().ctx.invoker.channel):
        self.channel = channel
        self.content = content
