"""MIT License

Copyright (c) 2022 EgorBron, Blusutils

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

import disnake
import os
import aeval
from roucore.bot import RoucBot
from disnake.ext import commands
from roucore.configuration import ConfigAcceptor

bot = RoucBot(ConfigAcceptor(seed=os.environ['ROUCSEED']))

@bot.listen(event='on_ready')
async def custom_ready_event():
    bot.logger.success('Hello world!')
    swstat = await bot.swish.ping() < 1000
    dbstat = await bot.get_database_status()
    bot.logger.debug(f'Swish is {swstat and "working" or "not responding"}. Database is {dbstat and "working" or "not responding"}.')

@bot.command(
    name = 'eval',
    aliases = ['evaulate', 'exec', 'execute', 'выполнитькод'], 
    #run_filters = [commands.filters.bot_owners_only], 
    brief = "bot.commands.eval.brief",
    description = 'bot.commands.eval.description'
)
async def __eval(ctx: commands.Context, *, to_eval: str = None):
    await aeval.aeval(to_eval)

bot.run()
