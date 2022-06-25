"""MIT License

Copyright (c) 2022 RouC Team, EgorBron, Blusutils

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from typing import Optional
import disnake
import os
import aeval
from roucore.bot import RoucBot
from disnake.ext import commands
from roucore.configuration import ConfigAcceptor

bot = RoucBot(os.path.abspath('./cogs'))#ConfigAcceptor(os.environ['ROUCFG']))
bot.remove_command('help')

@bot.listen(name='on_ready')
async def custom_ready_event():
    bot.logger.success('Hello world!')
    #dbstat = await bot.get_database_status()
    #bot.logger.debug(f'Database is dbstat and "working" or "not responding".')

@bot.command(
    aliases=['h', 'хелп', 'помощь']
)
async def help(ctx, command: Optional[str]):
    await ctx.send('Пока что help не работает\nFor now help isn\'t working')
    for cmd in bot.commands:
        pass

@bot.command(
    aliases = ['evaulate', 'exec', 'execute', 'выполнитькод'],
    #run_filters = [commands.filters.bot_owners_only], 
    brief = "bot.commands.eval.brief",
    description = 'bot.commands.eval.description'
)
async def eval(ctx: commands.Context, *, to_eval: str = None):
    if ctx.author.id not in bot.owner_ids: return await ctx.send(":x:")
    try: r = await aeval.aeval(to_eval, globals(), locals())
    except Exception as e: r = e
    await ctx.send(str(r))

@bot.command(name='load')
async def __cog_load(ctx: commands.Context, *, extname = ''):
    if extname == '':
        succ = bot.load_extensions()
        await ctx.send(embed=disnake.Embed(title='Multiple cogs load', description=f'Successful loads: {succ}/{len(os.listdir(bot.cogsdir))}'))

@bot.command()
async def delemotes(ctx: commands.Context):
    if ctx.author.id not in bot.owner_ids: return await ctx.send(":x:")
    for emoji in ctx.guild.emojis:
        await emoji.delete()
        await ctx.send(emoji.name+" deleted")

@bot.command()
async def moveemotes(ctx: commands.Context, target: disnake.Guild):
    if ctx.author.id not in bot.owner_ids: return await ctx.send(":x:")
    for emoji in ctx.guild.emojis:
        e = await target.create_custom_emoji(name=emoji.name, image=await emoji.read(), roles = emoji.roles, reason=f"Export emojis from {ctx.guild.name} ({ctx.guild.id})")
        await ctx.send(e.name+" created")

bot.run_safe()
