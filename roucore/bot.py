import disnake
import os
from roucore.configuration import ConfigAcceptor
from disnake.ext import commands
from locallibs import swish

class RoucBot(commands.Bot):
    def __init__(self):#, cfg_acceptor: ConfigAcceptor):
        """RouC Bot base

        Args:
            cfg_acceptor (ConfigAcceptor): Configuration acceptor
        """
        #d = cfg_acceptor.recrypt_and_get()
        self.creators = [555638466365489172]
        self.started_at = 0
        self.completed_commands_session = 0
        self.swish = swish
        intents = disnake.Intents(bans=True, emojis=True, guilds=True, members=True, voice_states=True, messages=True, reactions=True, presences=True)
        super().__init__(
            command_prefix = self.getprefix,
            intents = intents, 
            case_insensitive = True, 
            description = "RouC bot", 
            owner_ids = self.creators, 
            strip_after_prefix = True
        )
    @staticmethod
    async def getprefix(bot, message):
        return commands.when_mentioned_or('+') # multiprefix will be added soon

    def run_safe(self):
        self.run(os.environ['rouctoken'].split(';')[0])
