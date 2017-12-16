from typing import Generator

import requests

import errors
import sync_utils


class RuneClient:
    """ A client which can fetch information regarding a champion's optimal runes """
    HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0'}

    def __init__(self, session: requests.Session = None):
        self.session = requests.Session() if session is None else session
        self.rune_links = sync_utils.load_rune_file(self.session)

    def __get(self, url: str) -> str:
        """ Small helper method for a quick GET request """
        return self.session.get(url, headers=self.HEADERS).text

    # @staticmethod
    # def update_rune_file():
    #     """ Update the link list for champs (as it's being updated relatively frequently) """
    #

    def get_runes(self, champion_name: str) -> Generator:
        """ Returns a list of dicts of optimal runepages for a given champion 

        Data retrieved from Runeforge.gg """
        # Check whether input is valid
        champion_lower = champion_name.lower()
        if champion_lower not in self.rune_links:
            raise errors.ChampNotFoundError(champion_name)

        # Return the parsed result as a generator
        # return (sync_utils.parse_rune_html(x) for x in (self.__get(x) for x in self.rune_links[champion_lower]))

        for x in self.rune_links[champion_lower]:
            html = self.__get(x)
            yield sync_utils.parse_rune_html(html)
