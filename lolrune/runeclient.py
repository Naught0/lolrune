from typing import Tuple

import requests

import lolrune.utils as utils
from .errors import *


class RuneClient:
    """A client which allows you get a champion's optimal runes.

    Parameters
    ----------
    session : requests.Session, optional
        The main session which is used to make all requests.
        If one is not passed, one will be created.

    Attributes
    ----------
    rune_links : dict
        This is the data contained the .data/rune_links.json file.
        The structure is as follows::

            {
                "champion_name": [
                    "http://link_to_the_rune.page/",
                    "http://a_second_link_if.exists/"
                ]
            }
    """
    HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0'}
    URL = 'http://runeforge.gg/'

    def __init__(self, session: requests.Session = None):
        self.session = requests.Session() or session
        self.rune_links = utils.load_rune_file()
        # Create a proper rune_links.json if it's broken for some reason
        if self.rune_links is None:
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
        """A method which updates the .data/rune_links.json file and ``self.rune_links``.

        The Runeforge.gg site is frequently updating
        """
        self.rune_links = utils.parse_rune_links(self._get(self.URL))

    def get_runes(self, champion_name: str) -> Tuple[dict]:
        """The main method to retrieve optimal runes for a given champion.

        Parameters
        ----------
        champion_name : str
            Case insensitive name of the champion to get runes for.

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
        """
        # Check whether input is valid
        champion_lower = champion_name.lower()
        if champion_lower not in self.rune_links:
            raise ChampNotFoundError(champion_name)

        rune_list = []
        for x in self.rune_links[champion_lower]:
            html = self._get(x)
            rune_list.append(utils.parse_rune_html(html))

        return tuple(rune_list)
