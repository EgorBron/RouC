import disnake
import asyncio
from disnake.ext import commands, tasks
class Information(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def on_cog_load(self):
        self.bot.logger.debug('Cog "Profile" loaded')

def setup(bot):
    bot.add_cog(Information(bot))
    bot.logger.debug('Cog "Information" was added')
def teardown(bot):
    bot.logger.debug('Cog "Information" was removed')