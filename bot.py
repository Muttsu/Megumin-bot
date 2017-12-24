"""a wrapper for the discord client"""
import json
import discord


class Bot(discord.Client):
    """helper class whith some usefull functions"""
    def __init__(self, **kwargs):
        discord.Client.__init__(self)

        with open("config.json", "r") as file:
            config = json.load(file)
            file.close()
        self.commands = kwargs.pop("commands", {})
        self.admin_ids = config["admins"]
        self.aliases = config["aliases"]
        self.modules = config["modules"]
        self.command_prefix = config["prefix"]
        if isinstance(self.command_prefix, str):
            self.command_prefix = [self.command_prefix]
        self.token = config["token"]

    def init(self):
        """calls the discord.Client.run() method"""
        try:
            self.run(self.token)
        except RuntimeError:
            #todo log msg
            self.logout()
