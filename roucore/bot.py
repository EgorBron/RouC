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
import asyncpg
import ujson
from roucore.configuration import ConfigAcceptor
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
        # dict with translations
        self.translations: dict =  {}
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
        # postgresql db
        self.db: asyncpg.connection.Connection = None
        # gateway intents
        intents = disnake.Intents(bans=True, emojis=True, guilds=True, members=True, voice_states=True, messages=True, message_content=True, reactions=True, presences=True)
        # init bot
        super().__init__(
            command_prefix = self.getprefix,
            intents = intents, 
            case_insensitive = True, 
            description = "RouC bot", 
            owner_ids = self.creators, 
            strip_after_prefix = True
        )
    # multiprefix
    @staticmethod
    async def getprefix(bot, message):
        return ['+', bot.user.mention] # multiprefix will be added soon. also when_mentioned_or not working, idk why

    @staticmethod
    def connect_to_db(address, username, password):
        return asyncio.run()

    # same as "bot.run", but token is hidden from other code!
    def run_safe(self):
        self.run(os.environ['rouctoken'].split(';')[0])

    # load all translations
    def load_translations(self):
        if not os.path.exists('translations.json'):
            self.logger.error('Translations file not found!')
            raise OSError('Translations file not found!')
        with open('translations.json', 'r') as tf:
            self.translations = ujson.load(tf)

    # translate text for specified object
    def translate(self, source: typing.Union[disnake.Guild, disnake.User, int], source_string: str):
        #self.db.fetchrow()
        return ""

    # minify text for places with characters limit
    def _minify_text(self, visible_characters: int, limit: int, inp_text: typing.Any, source: typing.Union[disnake.Guild, disnake.User, int]):
        # sry guys, but... it made this in one line
        return f'{str(inp_text)[:visible_characters]}...\n...{self.translate(source, "bot.funcs.minify_text.first")} {len(str(inp_text).replace(str(inp_text)[visible_characters:], ""))} {self.translate(source, "bot.funcs.minify_text.second")}...' if len(str(inp_text)) >= limit else str(inp_text)

    # minify text for embeds "field value"
    def minify_text_1024(self, inp_text: typing.Any, source: typing.Union[disnake.Guild, disnake.User, int]):
       return self._minify_text(900, 1024, inp_text, source)

    # same as above, but for embeds "field name"
    def minify_text_256(self, inp_text: typing.Any, source: typing.Union[disnake.Guild, disnake.User, int]):
        return self._minify_text(132, 256, inp_text, source)

    # default events
    async def on_connect(self):
        self.logger.debug("Connected")
        threading.Thread(target=self.load_translations).run()
        self.db = await asyncpg.connect('postgresql://postgres@localhost/bots', user='roucbot', password='roucbottest')

    async def on_ready(self):
        self.logger.success("Started")
