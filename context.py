class Context:
    def __init__(self, **attrs):
        self.message = attrs.pop("message", None)
        self.bot = attrs.pop("bot", None)
    
    async def say(self, msg):
        return await self.bot.send_message(self.message.channel, msg)