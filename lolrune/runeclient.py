from typing import Tuple

import requests

from . import utils
from .errors import *
from .runepage import Champion


class RuneClient:
    """A client which allows you get a champion's optimal runes.
    You can find a brief example :ref:`here <rune_client_ex>`.

    Parameters
    ----------
    session : :class:`requests.Session`, optional
        The main session which is used to make all requests.
        If one is not passed, one will be created.

    Attributes
    ----------
    HEADERS : dict
        Firefox headers for the particular version used to inspect the html.

    URL : str
        The runeforge.gg url used in requests.

    rune_links : dict
        A dict containing all champ's individual rune pages.

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
    URL = 'http://runeforge.gg/'

    def __init__(self, session: requests.Session = None):
        self.session = session or requests.Session()
        self.rune_links = utils.parse_rune_links(self._get(self.URL))

    def _get(self, url: str) -> str:
        """A small wrapper method which makes a quick GET request.

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
        resp = self.session.get(url, headers=self.HEADERS)
        if resp.status_code is 200:
            return resp.text
        else:
            raise RuneConnectionError(resp.status_code)

    def update_champs(self):
        """A method which updates ``self.rune_links``.
        This is useful because runeforge.gg is frequently updating.

        Raises
        ------
        RuneConnectionError
            If the GET response status is not 200.
        """
        self.rune_links = utils.parse_rune_links(self._get(self.URL))

    def get_raw(self, champion_name: str) -> Tuple[dict]:
        """The main method to retrieve **raw** optimal runes for a given champion.

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
        # Check whether input is valid
        champion_lower = champion_name.lower()
        if champion_lower not in self.rune_links:
            raise ChampNotFoundError(champion_name)

        rune_list = []
        for x in self.rune_links[champion_lower]:
            html = self._get(x)
            rune_list.append(utils.parse_rune_html(html, x))

        return tuple(rune_list)

    def get_runes(self, champion_name: str) -> Tuple[Champion]:
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
            raise ChampNotFoundError(champion_name)

        return tuple(Champion(x) for x in self.get_raw(champion_lower))
