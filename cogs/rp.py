import disnake
import asyncio
import random
import os
import aiohttp, ujson
from roucore.bot import RoucBot
from disnake.ext import commands, tasks

class RoleplayMain(commands.Cog):
    def __init__(self, bot):
        self.bot: RoucBot = bot

    async def on_cog_load(self):
        self.bot.logger.debug('Cog "RoleplayMain" loaded')

    @commands.command(
        aliases=['try', 'попытаться', 'попробовать'],
        brief="bot.commands.trydo.brief",
        description="bot.commands.trydo.description"
    )
    async def trydo(self, ctx, *, do):
        translate = lambda s: self.bot.translate("bot.commands.trydo."+s, 'en') # alias
        result, coloring = (translate("body.success"), 0x55ff55) if random.choice((True, False)) else (translate("body.fail"), 0xff5555)
        await ctx.send(embed = disnake.Embed(title = f'{ctx.author.name} {translate("body.tryed")}:', description = f'*{do}*', color = coloring).add_field(name = f'{result}', value = '** **').set_author(name = str(ctx.author), icon_url = ctx.author.avatar.url))

    @commands.command()
    async def do(self, ctx, *, doing):
        await ctx.send(embed = disnake.Embed(title = f'{ctx.author.name}:', description = f'*{doing}*', color = 0x4a7dff).set_author(name = str(ctx.author), icon_url = ctx.author.avatar.url))

class RoleplayActions(commands.Cog):
    def __init__(self, bot):
        self.bot: RoucBot = bot

    async def on_cog_load(self):
        self.bot.logger.debug('Cog "RoleplayMain" loaded')

    async def get_tenor_gif(self, param):
        async with aiohttp.ClientSession(json_serialize=ujson):
            async with self.session.get(f"https://g.tenor.com/v1/search?q={param.replace(' ', '%20')}&key={os.environ.get('rouctoken').split(';')[6]}&limit=1000") as r:
                if r.status == 200:
                    async def trget(num):
                        try: return (await r.json())["results"][num]["media"][0]['gif']['url']
                        except IndexError: return await trget(random.randint(0, 1000))
                    await trget(random.randint(0, 1000))
                else:
                    return r.status
    
    async def build_embed(self, r, author, action, target=None):
        if target is not None:
            if author == target:
                return self.bot.errembed(self.bot.translate("bot.errors.self_inapplicable"))
        if not isinstance(r, int):
            return disnake.Embed(title=f"{author.name} {action} {target.name if target is not None else ''}", colour=self.bot.defaultcolor).set_image(url=r)
        else:
            return self.bot.errembed(self.bot.translate("bot.errprs.unexpected_error").format(self.bot.translate("bot.errors.errcode").format(r)))

def setup(bot):
    bot.add_cog(RoleplayMain(bot))
    bot.logger.debug('Cog "RoleplayMain" added')
def teardown(bot):
    bot.logger.debug('Cog "Roleplay" removed')