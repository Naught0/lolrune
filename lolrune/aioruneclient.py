import aiohttp
import asyncio
from typing import Generator

import lolrune.utils as utils
from .errors import *


class AioRuneClient:
    """ A non-blocking client which can fetch information regarding a champion's
    optimal rune pages """
    HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0'}
    URL = 'http://runeforge.gg'

    def __init__(self, session: aiohttp.ClientSession = None, loop: asyncio.AbstractEventLoop = none):
        self.loop = asyncio.get_event_loop() if loop is None else loop
        self.session = aiohttp.ClientSession(loop=self.loop) if session is None else session
        self.rune_links = utils.load_rune_file()
        if self.rune_links is None:
            self.rune_links = utils.parse_rune_links(
                self.loop.run_until_complete(self.__get(self.URL)))

    async def __get(self, url: str) -> str:
        """ A small helper method for a quick GET request """
        async with self.session.get(url, headers=self.HEADERS) as r:
            return await r.text()

    async def update_champs(self):
        """ Update the rune_links.json file
        (as the website is being updated relatively frequently) """
        html = await self.__get(self.URL)
        utils.parse_rune_links(html)

    async def get_runes(self, champion_name: str) -> Generator:
        """ Returns an async generator which yields runepages in dict form for a given champion

        Data retrieved from Runeforge.gg """
        champion_lower = champion_name.lower()
        if champion_lower not in self.rune_links:
            raise ChampNotFoundError(champion_name)
            return

        for x in self.rune_links[champion_lower]:
            html = await self.__get(x)
            yield utils.parse_rune_html(html)