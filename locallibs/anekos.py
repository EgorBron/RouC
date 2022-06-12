"""Async NekosAPI interactor

MIT License

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
import aiohttp, asyncio
import ujson
# import blusutils
# from blusutils.collections import deep_merge

# possible = [
#     'feet', 'yuri', 'trap', 'futanari', 'hololewd', 'lewdkemo',
#     'solog', 'feetg', 'cum', 'erokemo', 'les', 'wallpaper', 'lewdk',
#     'ngif', 'tickle', 'lewd', 'feed', 'gecg', 'eroyuri', 'eron',
#     'cum_jpg', 'bj', 'nsfw_neko_gif', 'solo', 'kemonomimi', 'nsfw_avatar',
#     'gasm', 'poke', 'anal', 'slap', 'hentai', 'avatar', 'erofeet', 'holo',
#     'keta', 'blowjob', 'pussy', 'tits', 'holoero', 'lizard', 'pussy_jpg',
#     'pwankg', 'classic', 'kuni', 'waifu', 'pat', '8ball', 'kiss', 'femdom',
#     'neko', 'spank', 'cuddle', 'erok', 'fox_girl', 'boobs', 'random_hentai_gif',
#     'smallboobs', 'hug', 'ero', 'smug', 'goose', 'baka', 'woof'
# ]

everywhere = ['tickle', 'waifu', 'baka', 'ngif', 'cuddle', 'avatar', 'holo', 'kiss', 'fox_girl', 'poke', 'goose', 'pat', 'slap', 'woof', 'wallpaper', 'hug', 'smug']

nsfw = [
    'feet', 'yuri', 'trap', 'futanari', 'hololewd', 'lewdkemo',
    'solog', 'feetg', 'cum', 'erokemo', 'les', 'lewdk', 'lewd', 'feed', 'gecg', 'eroyuri', 'eron',
    'cum_jpg', 'bj', 'nsfw_neko_gif', 'solo', 'kemonomimi', 'nsfw_avatar',
    'gasm', 'anal', 'hentai', 'erofeet',
    'keta', 'blowjob', 'pussy', 'tits', 'holoero', 'lizard', 'pussy_jpg',
    'pwankg', 'classic', 'kuni', 'femdom',
    'neko', 'spank', 'erok', 'boobs', 'random_hentai_gif',
    'smallboobs', 'ero'
]

possible = [].extend(everywhere).extend(nsfw)

class NekoException(Exception):
    """Base exception class for anekos.py """
    pass
class NothingFound(NekoException):
    """ The API didn't return anything """
    pass
class EmptyArgument(NekoException):
    """ When no target is defined """
    pass
class InvalidArgument(NekoException):
    """ Invalid argument within the category """
    pass

class NekosAsyncAPI:
    def __init__(self, base_url, **kwargs):
        self.base_url = base_url
        # for arg in kwargs:
        #     if isinstance(kwargs[arg], dict):
        #         kwargs[arg] = deep_merge(getattr(self.session, arg), kwargs[arg])
        #     setattr(self.session, arg, kwargs[arg])

    async def get(self, url, **kwargs):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.base_url+url, **kwargs) as resp:
                return resp

    async def post(self, url, **kwargs):
        async with aiohttp.ClientSession() as session:
            async with session.post(self.base_url+url, **kwargs) as resp:
                return resp

    async def get_as_json(self, url, **kwargs):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.base_url+url, **kwargs) as resp:
                return await resp.json() # похуй на южсон, когда пофиксим - верну



napi = NekosAsyncAPI("https://nekos.life/api/v2")

async def img(target: str) -> str:
    """Get image from Nekos API

    Args:
        target (str): Category to get

    Raises:
        EmptyArgument: When you pass argument not as string, or when don't pass ше
        InvalidArgument: When you use invalid category
        NothingFound: When API doesn't work or gave wrong response

    Returns:
        str: URL of image under requested category
    """

    if target is None:
        raise EmptyArgument("You have to at least define an argument in string format\nArguments: {}".format(possible))
    if target.lower() not in possible:
        raise InvalidArgument("You haven't added any valid arguments\nArguments: {}".format(possible))
    try:
        if target.lower() == "random_hentai_gif":
            r = await napi.get_as_json("/img/Random_hentai_gif")
        else:
            r = await napi.get_as_json("/img/" + target.lower())
    except Exception as e:
        raise
        # raise NothingFound("Couldn't contact the API right now...")

    return r["url"] 
