import json
import re

from bs4 import BeautifulSoup


def parse_rune_links(html: str) -> dict:
    """A function which parses the main Runeforge website into dict format.

    Parameters
    ----------
    html : str
        The string representation of the html obtained via a GET request.

    Returns
    -------
    dict
        The nested rune_links champ rune pages from runeforge.
    """
    soup = BeautifulSoup(html, 'lxml')

    # Champs with only a single runepage
    single_page_raw = soup.find_all('li', class_='champion')
    single_page = {re.split('\W+', x.a.div.div['style'])[-3].lower():
                       [x.a['href']] for x in single_page_raw if x.a is not None}

    # Champs with two (or more) runepages
    double_page_raw = soup.find_all('div', class_='champion-modal-open')
    # This is JSON data which just needs to be decoded
    double_page_decode = [json.loads(x['data-loadouts']) for x in double_page_raw]
    # This lowers the champ name in the structure, 
    # and pulls out the champ links, after it's been decoded
    double_page = {re.sub('[^A-Za-z0-9]+', '', x[0]['champion'].lower()):
                       [x[0]['link'], x[1]['link']] for x in double_page_decode}

    # Combine the two dicts
    champs_combined = {**single_page, **double_page}

    # Scraping yields "wukong" to be "monkeyking" for whatever reason
    # I have yet to find any more anomalies like this
    champs_combined['wukong'] = champs_combined.pop('monkeyking')

    return champs_combined


def parse_rune_html(html: str, url: str) -> dict:
    """A function that returns a dict representation of the Runeforge.gg page for a specific champ

    Parameters
    ----------
    html : str
        The string representation of the html obtained via a GET request

    url : str
        The URL for the runeforge page being parsed.

    Returns
    -------
    dict
        Contains champ rune info described in ``RuneClient`` and ``AioRuneClient``.
    """
    soup = BeautifulSoup(html, 'lxml')

    # The soup stuff
    champ = soup.find('h1', class_='champion-header--title').text
    title = soup.find('h2', class_='loadout-title').text
    description = soup.find('p').text
    # Names of the Rune trees
    p_tree, s_tree = [x.text for x in soup.find_all('h2', class_='rune-path--name')]
    # List of all the runes together
    all_runes = soup.find_all('a', class_='rune-name')
    # The keystone (duh)
    keystone = all_runes[0].text
    # Rest of the runes in the primary tree, sans keystone
    p_rest = [x.text for x in all_runes[1:4]]
    # The runes in the secondary tree
    s_rest = [x.text for x in all_runes[4:7]]

    return {'name': champ, 'title': title, 'description': description, 'url': url,
            'runes': {'primary': {'name': p_tree, 'keystone': keystone, 'rest': p_rest},
                      'secondary': {'name': s_tree, 'rest': s_rest}}}
