from typing import Generator
import requests
import json
import errors
import utils


class RuneClient:
    """ A client which can fetch information regarding a champion's optimal runes """
    HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0'}

    def __init__(self, session: requests.Session = None):
        self.session = requests.Session() if session is None else session
        self.rune_links = utils.load_rune_file()
        # Create a proper rune_links.json if it's broken for some reason
        if self.rune_links is None:
            self.rune_links = utils.get_rune_links(self.__get('http://runeforge.gg'))

    def __get(self, url: str) -> str:
        """ Small helper method for a quick GET request """
        return self.session.get(url, headers=self.HEADERS).text

    @staticmethod
    def update_rune_file():
        """ Update the rune_links.json file 
        (as the website is being updated relatively frequently) """
        utils.get_rune_links(self.__get('https://runeforge.gg'))

    def get_runes(self, champion_name: str) -> Generator:
        """ Returns generator which yields runepages in dict form for a given champion 

        Data retrieved from Runeforge.gg """
        # Check whether input is valid
        champion_lower = champion_name.lower()
        if champion_lower not in self.rune_links:
            raise errors.ChampNotFoundError(champion_name)

        for x in self.rune_links[champion_lower]:
            html = self.__get(x)
            yield sync_utils.parse_rune_html(html)
