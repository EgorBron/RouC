import disnake
import asyncio
from disnake.ext import commands, tasks
from roucore.bot import RoucBot
class Profile(commands.Cog):
    def __init__(self, bot: RoucBot):
        self.bot: RoucBot = bot

    async def on_cog_load(self):
        self.bot.logger.debug('Cog "Profile" loaded')

    @commands.command()
    async def avatar(self, ctx: commands.Context, member = None):
        try: 
            member = await commands.converter.MemberConverter().convert(ctx, member) if member is not None else ctx.author
            avemb = disnake.Embed(
                title=self.bot.translate('bot.commands.avatar.body.author_avatar') if ctx.author == member else self.bot.translate('bot.commands.avatar.body.author_avatar').format(str(member)),
                colour=self.bot.defaultcolor)\
            .set_image(url=member.avatar.url if member is not None else ctx.author.avatar.url)
            await ctx.send(embed=avemb)
        except commands.errors.MemberNotFound:
            await ctx.send(embed=self.bot.errembed(self.bot.translate('bot.errors.unknown_member').format(member)))

def setup(bot):
    bot.add_cog(Profile(bot))
    bot.logger.debug('Cog "Profile" was added')
def teardown(bot):
    bot.logger.debug('Cog "Profile" was removed')