import json
from typing import Union

from bs4 import BeautifulSoup


def load_rune_file() -> Union[dict, None]:
    """A function which loads the .data/rune_links.json file.

    Returns
    -------
    Union[dict, None]
        - ``dict`` if there are no errors in opening the file.
        - ``None`` otherwise.
    """
    try:
        with open('rune_links.json') as f:
            links = json.load(f)

    except (FileNotFoundError, json.JSONDecodeError):
        return None

    return links


def parse_rune_links(html: str) -> dict:
    """A function which parses the main Runeforge website into the .data/rune_links.json format.

    Parameters
    ----------
    html : str
        The string representation of the html obtained via a GET request

    Returns
    -------
    dict
        The rune_links.json file
    """
    soup = BeautifulSoup(html, 'lxml')

    # Champs with only a single runepage
    single_champs_raw = soup.find_all('li', class_='champion')
    single_champs = {x.a.div.div['style'][77:-6].lower(): [x.a['href']] for x in single_champs_raw if x.a is not None}

    # Champs with two (or more) runepages
    double_champs_raw = soup.find_all('div', class_='champion-modal-open')
    double_champs_decode = [json.loads(x['data-loadouts']) for x in double_champs_raw]
    double_champs = {x[0]['champion'].lower(): [x[0]['link'], x[1]['link']] for x in double_champs_decode}

    # Combine the two dicts
    champs_combined = {**single_champs, **double_champs}

    # Write to data file
    with open('rune_links.json', 'w') as f:
        json.dump(champs_combined, f, indent=2, sort_keys=True)

    return champs_combined


def parse_rune_html(html: str) -> dict:
    """A function that returns a dict representation of the Runeforge.gg page for a specific champ

    Parameters
    ----------
    html : str
        The string representation of the html obtained via a GET request

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

    return {'name': champ, 'title': title, 'description': description,
            'runes': {'primary': {'name': p_tree, 'keystone': keystone, 'rest': p_rest},
                      'secondary': {'name': s_tree, 'rest': s_rest}}}
