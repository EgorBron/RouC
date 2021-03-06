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
import asyncio
import threading
import typing
import disnake
import os, sys
import jinja2
from motor.motor_asyncio import AsyncIOMotorClient
import ujson
from roucore.configuration import ConfigAcceptor
from roucore.localization import Localizator
from disnake.ext import commands
from loguru import logger

class RoucBot(commands.Bot):
    def __init__(self):#, cfg_acceptor: ConfigAcceptor):
        """RouC Bot base

        Args:
            cfg_acceptor (ConfigAcceptor): Configuration acceptor
        """
        #d = cfg_acceptor.recrypt_and_get()
        # list of "owners" for bot based on this code
        self.creators = [555638466365489172]
        # default embeds color
        self.defaultcolor = 0x2813fb
        # dict with translations
        self.translations = Localizator()
        # # directory contains cogs
        # self.cogsdir = cogs_dir#+'/' if not cogs_dir.endswith('/') else cogs_dir
        # for "uptime" feature (combined with process start time from psutil.Process().create_time)
        self.started_at: int = 0
        # for "botinfo"
        self.completed_commands_session: int = 0
        # loguru logger
        try: logger.remove(0)
        except ValueError: pass
        logger.add(sys.stdout, level = 'INFO', format = '<WHITE><black>[{time:YYYY-MM-DD HH:mm:ss}]</black></WHITE> <level>{level}</level>: at <magenta><underline>{file}</underline></magenta> (<cyan>{function}</cyan>, line <yellow>{line}</yellow>):\n\t{message}', colorize = True, backtrace = False, diagnose = True, enqueue = True)
        logger.add('rouc_logs/log_{time:YYYY-MM-DD}.log', level = 'DEBUG', format = '[{time:YYYY-MM-DD HH:mm:ss}] {level}: at {file} ({function}, line {line}):\n\t{message}', colorize = False, backtrace = False, diagnose = True, enqueue = True, encoding = 'utf-8')
        self.logger = logger
        # mongodb
        self.db: AsyncIOMotorClient = AsyncIOMotorClient('mongodb://localhost:27017').roucdb
        # gateway intents
        intents = disnake.Intents(bans=True, emojis=True, guilds=True, members=True, voice_states=True, messages=True, message_content=True, reactions=True, presences=True)
        # init bot
        super().__init__(
            command_prefix = '+',
            intents = intents, 
            case_insensitive = True, 
            description = "RouC bot", 
            owner_ids = self.creators, 
            strip_after_prefix = True
        )
    # multiprefix
    async def get_prefix(self, message):
        prefix = await self.db.guilds.find_one({'id': message.guild.id})
        prefix = prefix['prefix'] if prefix is not None else '+'
        return [prefix, self.user.mention] # when_mentioned_or not working, idk why

    # same as "bot.run", but token is hidden from other code!
    def run_safe(self):
        self.run(os.environ['rouctoken'].split(';')[0])

    # load all translations
    def load_translations(self):
        if not os.path.exists('translations.json'):
            self.logger.error('Translations file not found!')
            raise OSError('Translations file not found!')
        self.translations.load('translations.json')

    # translate text for specified object
    def translate(self, source_string: str, source_language = 'en') -> str:
        #self.db.fetchrow()
        #srclang = asyncio.run(self.getlocale(source))
        return self.translations.get(source_string)[source_language]

    # async def getlocale(self, source: typing.Union[disnake.Guild, disnake.User, int]):
    #     source = self.get_guild(source) if isinstance(source, int) else source
    #     if isinstance(source, disnake.Guild):
    #         await self.db.fetchrow("SELECT locale FROM guilds")

    async def getlang(self, guild: disnake.Guild):
        result = await self.db.guilds.find_one({'id': guild.id})
        return result['locale'] if result is not None else 'en'

    # minify text for places with characters limit
    def _minify_text(self, visible_characters: int, limit: int, inp_text: typing.Any, source_language='en'):
        # sry guys, but... it made this in one line
        return f'{str(inp_text)[:visible_characters]}...\n...{self.translate("bot.funcs.minify_text.first", source_language)} {len(str(inp_text).replace(str(inp_text)[visible_characters:], ""))} {self.translate("bot.funcs.minify_text.second", source_language)}...' if len(str(inp_text)) >= limit else str(inp_text)

    # minify text for embeds "field value"
    def minify_text_1024(self, inp_text: typing.Any, source_language='en'):
       return self._minify_text(900, 1024, inp_text, source_language)

    # same as above, but for embeds "field name"
    def minify_text_256(self, inp_text: typing.Any, source_language='en'):
        return self._minify_text(132, 256, inp_text, source_language)

    # prepare error embed
    def errembed(self, errtxt: str, srclang: str = 'en'):
        return disnake.Embed(title=f'RouC | {self.translate("bot.errors.errword", srclang)}', description=errtxt, color=0xfb3613).set_footer(text=self.translate('bot.copyright'))

    # prepare success embed
    def succembed(self, succtxt: str, srclang: str = 'en'):
        return disnake.Embed(title=f'RouC | {self.translate("bot.success", srclang)}', description=succtxt, color=0x13fb14).set_footer(text=self.translate('bot.copyright'))

    # own cogs loaders
    def load_extension(self, extension):
        try:
            super(commands.Bot, self).load_extension(f'cogs.{extension}' if not extension.startswith('cogs.') else extension)
            return
        except commands.ExtensionAlreadyLoaded:
            self.logger.error(f"'{extension}' already loaded. Skipped")
            return "already_loaded"
        except commands.NoEntryPointError:
            self.logger.error(f"'{extension}' does not have entrypoint function (setup). Skipped")
            return "no_entrypoint"
        except (ImportError, commands.errors.ExtensionNotFound):
            self.logger.error(f"'{extension}' not found. Skipped")
            return "not_found"
        except Exception as e:
            self.logger.error(f"'{extension}' has an error. Skipped. Error (no stack traceback):\n\t\t{e}")
            return e

    def load_extensions(self):
        success_loads = 0
        for extension in disnake.utils.search_directory('./cogs'):
            if self.load_extension(extension) is None:
                success_loads += 1
        return success_loads

    # same as above, but for unloading
    def unload_extension(self, extension):
        try:
            super().unload_extension(f'cogs.{extension}')
            return
        except commands.ExtensionNotLoaded:
            self.logger.error(f"'{extension}' already unloaded. Skipped")
            return "already_unloaded"
        except (ImportError, commands.errors.ExtensionNotFound):
            self.logger.error(f"'{extension}' not found. Skipped")
            return "not_found"
        except Exception as e:
            self.logger.error(f"'{extension}' has an error. Skipped. Error (no stack traceback):\n\t\t{e}")
            return e

    def unload_extensions(self):
        success_unloads = 0
        for extension in self.cogs:
            if self.unload_extension(f'cogs.{extension}') is None:
                success_unloads += 1
        return success_unloads

    # database management functions

    # insert guild to db
    async def insert_guild_to_db(self, guild: disnake.Guild):
        ret = await self.db.guilds.insert_one({
            'id': guild.id,
            'prefix': '+',
            'locale': 'en',
            'preferences': {},
            'channelsprefs': {},
            'warns': {},
            'automod': {}
        })
        if self.intents.members:
            for member in guild.members:
                if member.bot: continue
                guildobj = {
                    'id': member.guild.id,
                    'last_nickname': member.display_name,
                    'last_roles': list(map(lambda r: r.id, member.roles)),
                    'bio': '',
                    'level': 0,
                    'xp': 0,
                    'can_setup': False,
                    'moderator': False,
                    'rulesets': {}
                }
                if (await self.db.users.find_one({'id': member.id})) is not None:
                    await self.db.users.update_one({'id': member.id}, {"$push": {'guilds': guildobj}})
                else:
                    await self.db.users.insert_one({
                        'id': member.id,
                        'blacklisted': False,
                        'notifications_level': 1,
                        'guilds': [guildobj]
                    })
        return ret

    # default events
    async def on_connect(self):
        self.logger.debug("Connected")
        threading.Thread(target=self.load_translations).run()

    async def on_ready(self):
        self.load_extensions()
        self.logger.success("Started")

    async def on_disconnect(self):
        #self.db.close()
        self.logger.info("Disconnected")

    async def on_guild_join(self, guild: disnake.Guild):
        if (await self.db.guilds.find_one({'id': guild.id})) is None:
            await self.insert_guild_to_db(guild)
        # here will be another stuff

    async def on_message(self, message: disnake.Message):
        # checks to prevent some errors and bugs
        if message.guild is None: return
        if message.author.bot: return
        # process command if it exists
        if (await self.get_context(message)).command in self.commands: return await self.process_commands(message)
        # guild object from database
        guildobj = dict(await self.db.guilds.find_one({'id': message.guild.id}))
            

    async def on_command(self, ctx: commands.Context):
        if ctx.command not in self.commands: return
        lang = await self.getlang(ctx.guild)
        if (await self.db.users.find_one({'id': ctx.author.id}))['blacklisted']:
            return await ctx.send(embed=self.errembed(self.translate('bot.errrors.blacklisted', lang), lang))
