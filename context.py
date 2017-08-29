class Context:
    def __init__(self, **attrs):
        self.message = attrs.pop("message", None)
        self.bot = attrs.pop("bot", None)