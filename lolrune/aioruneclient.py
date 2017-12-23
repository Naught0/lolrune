import asyncio
from typing import Tuple

import aiohttp

from . import utils
from .runepage import Champion 
from .errors import *


class AioRuneClient:
    """An asynchronous version of :class:`RuneClient` used to fetch optimal runes for champions.
    You can find a brief example :ref:`here <aio_client_ex>`.

    Parameters
    ----------
    session : :class:`aiohttp.ClientSession`, optional
        The aiohttp session used in all requests. If none is provided,
        a new session will be created.

    loop : :class:`asyncio.AbstractEventLoop`, optional
        The asyncio event loop. If none is provided, a new loop will be created.

    Attributes
    ----------
    HEADERS : dict
        Firefox headers for the particular version used to inspect the html.

    URL : str
        The runeforge.gg url used in requests.

    rune_links : dict
        This is the data contained in the rune_links.json file.

    Note
    ----
    The rune_links data is structured like so::

        {
          "aatrox": [
            "http://runeforge.gg/loadouts/die-and-be-forgotten/"
          ],
          "ahri": [
            "http://runeforge.gg/loadouts/the-poking-fox/",
            "http://runeforge.gg/loadouts/burst-snowball-carry/"
          ], ...
        }
    """
    HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0'}
    URL = 'http://runeforge.gg'

    def __init__(self, session: aiohttp.ClientSession = None, loop: asyncio.AbstractEventLoop = None):
        self.loop = loop or asyncio.get_event_loop()
        self.session = session or aiohttp.ClientSession(loop=self.loop)
        self.rune_links = utils.load_rune_file()
        # TODO:
        # Make this not awful by removing run_until_complete
        if self.rune_links is None:
            self.rune_links = utils.parse_rune_links(self.loop.run_until_complete(
                self._get(self.URL)))

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
        This is useful because runeforge.gg is frequently updating.

        Raises
        ------
        RuneConnectionError
            If the request does not return with a status of 200.
        """
        html = await self._get(self.URL)
        self.rune_links = utils.parse_rune_links(html)

    async def get_raw(self, champion_name: str) -> Tuple[dict]:
        """A method to retrieve **raw** optimal runes for a given champion.

        Parameters
        ----------
        champion_name : str
            Case insensitive name of the champion to get runes for.

        Returns
        -------
        Tuple[dict]
            A tuple of dicts which contain the rune information.

        Note
        ----
        Please see :ref:`raw_return_formatting` for more information on the return type.

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

    async def get_runes(self, champion_name: str) -> Tuple[Champion]:
        """A method to retrieve a champion's runepage objects.
        
        Parameters
        ----------
        champion_name : str
            Case insensitive name of the champion to get runes for.
        
        Returns
        -------
        Tuple[:class:`Champion`]
            A tuple of :class:`Champion`\s. 

        Note
        ----
        Please see :ref:`abs_return_formatting` and :class:`Champion` for more information on the return type.

        Raises
        ------
        ChampNotFoundError
            If the champion is not found in ``self.rune_links``.
        """
        champion_lower = champion_name.lower()
        if champion_lower not in self.rune_links:
            raise ChampNotFoundError(champ_name)

        return tuple(Champion(x) for x in await self.get_raw(champion_lower))
