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

bot = RoucBot()#ConfigAcceptor(os.environ['ROUCFG']))
bot.remove_command('help')

@bot.command(
    aliases=['h', 'хелп', 'помощь']
)
async def help(ctx, command: Optional[str]):
    await ctx.send('Пока что help не работает\nFor now help isn\'t working')
    for cmd in bot.commands:
        pass

@bot.command()
async def setlocale(ctx: commands.Context, locale: str = None):
    if not ctx.author.guild_permissions.administrator:
        return await ctx.send(embed=bot.errembed(bot.translate('bot.errors.missing_user_permissions').format('administrator')))
    if locale is None:
        return await ctx.send(embed=bot.errembed(bot.translate('empty_locale')))
    if locale not in bot.translations.get('available_locales'):
        return await ctx.send(embed=bot.errembed(bot.translate('unsupported_locale').format(locale, ", ".join(bot.translations.get('available_locales')))))
    await bot.db.guilds.update_one({'id': ctx.guild.id}, {"$set": {"locale": locale}})
    await ctx.send(embed=bot.succembed(bot.translate('locale_set_success', locale).format(locale), locale))

@bot.command()
async def setprefix(ctx: commands.Context, prefix: str = None):
    lang = await bot.getlang(ctx.guild)
    if not ctx.author.guild_permissions.administrator:
        return await ctx.send(embed=bot.errembed(bot.translate('bot.errors.missing_user_permissions', lang).format('administrator'), lang))
    if prefix is None:
        return await ctx.send(embed=bot.errembed(bot.translate('bot.errrors.missed_argument', lang), lang))
    await bot.db.guilds.update_one({'id': ctx.guild.id}, {"$set": {"prefix": prefix}})
    await ctx.send(embed=bot.succembed(bot.translate('bot.commands.setprefix.body.success_set', lang).format(prefix), lang))

@bot.command(
    aliases = ['evaulate', 'exec', 'execute', 'выполнитькод'],
    #run_filters = [commands.filters.bot_owners_only], 
    brief = "bot.commands.eval.brief",
    description = 'bot.commands.eval.description'
)
async def eval(ctx: commands.Context, *, to_eval: str = None):
    if ctx.author.id not in bot.owner_ids: return await ctx.send(":x:")
    globs = globals()
    globs['ctx'] = ctx
    try: r = await aeval.aeval(to_eval, globs, locals())
    except Exception as e: r = e
    await ctx.send(str(r))

@bot.command()
async def insertguild(ctx: commands.Context, guilds: commands.Greedy[disnake.Guild]):
    if ctx.author.id not in bot.owner_ids: return await ctx.send(":x:")
    if len(guilds) == 0: guilds = [ctx.guild]
    for guild in guilds:
        if (await bot.db.guilds.find_one({'id': guild.id})) is None:
            r = await bot.insert_guild_to_db(guild)
            await ctx.send(f'Guild {guild.id} ({guild.name}) successfully inserted')
        else: await ctx.send(f'Guild {guild.id} ({guild.name}) already inserted')

def load_text(result):
    if result is None:
        return "Cog successfully loaded"
    elif result == "not_found":
        return "Failed to load: cog not found"
    elif result == "already_loaded":
        return "Failed to load: cog already loaded"
    elif result == "no_entrypoint":
        return "Failed to load: cog does not have entrypoint (setup function)"
    elif isinstance(result, Exception):
        return "Failed to load: cog raised an error. More info in console output"
@bot.command(name='load')
async def __cog_load(ctx: commands.Context, *, extname = ''):
    if extname == '':
        succ = bot.load_extensions()
        await ctx.send(embed=disnake.Embed(title='Multiple cogs load', description=f'Successful loads: {succ}/{len(os.listdir(bot.cogsdir))}'))
    else:
        result = bot.load_extension(extname)
        color = result is None and 0x00ff00 or 0xff0000
        result = load_text(result)
        await ctx.send(embed=disnake.Embed(title="Cog load - "+extname, description=result, color=color))

def unload_text(result):
    if result is None:
        return "Cog successfully unloaded"
    elif result == "not_found":
        return "Failed to unload: cog not found"
    elif result == "already_unloaded":
        return "Failed to unload: cog already unloaded"
    elif isinstance(result, Exception):
        return "Failed to load: cog raised an error. More info in console output"

@bot.command(name='unload')
async def __cog_unload(ctx: commands.Context, *, extname = ''):
    if extname == '':
        allcogs = len(bot.cogs.keys())
        succ = bot.unload_extensions() 
        await ctx.send(embed=disnake.Embed(title='Multiple cogs unload', description=f'Successful loads: {succ}/{allcogs}'))
    else:
        result = bot.unload_extension(extname)
        color = result is None and 0x00ff00 or 0xff0000
        result = unload_text(result)
        await ctx.send(embed=disnake.Embed(title="Cog unload - "+extname, description=result, color=color))

@bot.command(name='reload')
async def __cog_reload(ctx: commands.Context, *, extname = ''):
    if extname == '':
        allcogs = len(bot.cogs.keys())
        succ_ul = bot.unload_extensions() 
        succ_l = bot.load_extensions()
        await ctx.send(embed=disnake.Embed(title='Multiple cogs reload', description=f'Successful unloads: {succ_ul}/{allcogs}\nSuccessful loads: {succ_l}/{len(os.listdir(bot.cogsdir))}'))
    else:
        result = bot.unload_extension(extname)
        if result is not None:
            return await ctx.send(embed=disnake.Embed(title="Cog reload - "+extname, description=f"Failed during unload: {unload_text(result)}", color=0xff0000))
        result = bot.load_extension(extname)
        if result is not None:
            return await ctx.send(embed=disnake.Embed(title="Cog reload - "+extname, description=f"Failed during load: {unload_text(result)}", color=0xff0000))
        await ctx.send(embed=disnake.Embed(title="Cog reload - "+extname, description=f"Cog successfully reloaded", color=0x00ff00))
        


# @bot.command()
# async def delemotes(ctx: commands.Context):
#     if ctx.author.id not in bot.owner_ids: return await ctx.send(":x:")
#     for emoji in ctx.guild.emojis:
#         await emoji.delete()
#         await ctx.send(emoji.name+" deleted")

@bot.command()
async def moveemotes(ctx: commands.Context, target: disnake.Guild):
    if ctx.author.id not in bot.owner_ids: return await ctx.send(":x:")
    for emoji in ctx.guild.emojis:
        e = await target.create_custom_emoji(name=emoji.name, image=await emoji.read(), roles = emoji.roles, reason=f"Export emojis from {ctx.guild.name} ({ctx.guild.id})")
        await ctx.send(e.name+" created")
try:
    bot.run_safe()
except RuntimeError:
    pass
