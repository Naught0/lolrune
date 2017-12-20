import asyncio
from typing import Tuple

import aiohttp

import lolrune.utils as utils
from .errors import *


class AioRuneClient:
    """An asynchronous version of the RuneClient used to fetch optimal runes for a champ

    Parameters
    ----------
    session : aiohttp.ClientSession, optional
        The aiohttp session used in all requests. If none is provided, a new aiohttp.ClientSession will be created.

    loop : asyncio.AbstractEventLoop, optional
        The asyncio event loop. If none is provided, a new loop will be created.

    Attributes
    ----------
    HEADERS : dict
        Firefox headers for the particular version used to inspect the html.

    URL : str
        The runeforge.gg url used in requests.

    rune_links : dict
        This is the data contained in the rune_links.json file.
    """
    HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0'}
    URL = 'http://runeforge.gg'

    def __init__(self, session: aiohttp.ClientSession = None, loop: asyncio.AbstractEventLoop = None):
        self.loop = asyncio.get_event_loop() or loop
        self.session = aiohttp.ClientSession(loop=self.loop) or session
        self.rune_links = utils.load_rune_file()
        if self.rune_links is None:
            self.rune_links = utils.parse_rune_links(
                self.loop.run_until_complete(self._get(self.URL)))

    async def _get(self, url: str) -> str:
        """A small wrapper method which makes a quick GET request

        Parameters
        ----------
        url : str
            The URL to get.

        Returns
        -------
        str
            The raw html of the requested page.

        Raises
        ------
        RuneConnectionError
            If the GET response status is not 200.
        """
        async with self.session.get(url, headers=self.HEADERS) as r:
            if r.status == 200:
                return await r.text()
            else:
                raise RuneConnectionError(r.status)

    async def update_champs(self):
        """A method which updates the rune_links.json file and ``self.rune_links``.

        The Runeforge.gg site is frequently updating
        """
        html = await self._get(self.URL)
        self.rune_links = utils.parse_rune_links(html)

    async def get_runes(self, champion_name: str) -> Tuple[dict]:
        """The main method to retrieve optimal runes for a given champion.

        Parameters
        ----------
        champion_name : str
            Case insensitive name of the champion to get runes for

        Returns
        -------
        Tuple[dict]
            A tuple of dicts which contain the Runeforge data. Below is an example of Runeforge data
            contained in the dict::

                {
                    "name": "Varus",
                    "title": "Bloodshed Carries a Price",
                    "description": "Lethality focused long range poke with [Q].",
                    "runes": {
                        "primary": {
                            "name": "Sorcery",
                            "keystone": "Arcane Comet",
                            "rest": [
                                "Manaflow Band",
                                "Celerity",
                                "Scorch"
                            ]
                        },
                        "secondary": {
                            "name": "Precision",
                            "rest": [
                                "Triumph",
                                "Coup De Grace"
                            ]
                        }
                    }
                }

        Raises
        ------
        ChampNotFoundError
            If the champion is not found in ``self.rune_links``.
        """
        champion_lower = champion_name.lower()
        if champion_lower not in self.rune_links:
            raise ChampNotFoundError(champion_name)

        rune_list = []
        for x in self.rune_links[champion_lower]:
            html = await self._get(x)
            rune_list.append(utils.parse_rune_html(html))

        return tuple(rune_list)
