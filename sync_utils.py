import json

import requests
from bs4 import BeautifulSoup


def load_rune_file(session: requests.Session, headers: dict = None) -> dict:
    """ Loads and returns the rune_file or fetches it using requests if it's not found """
    path = 'data/rune_links.json'
    try:
        with open(path) as f:
            links = json.load(f)

    except (FileNotFoundError, json.JSONDecodeError):
        links = get_champ_json(session, headers=headers)
        with open(path, 'w') as f:
            json.dump(links, f, sort_keys=True, indent=2)

    return links


def get_champ_json(session: requests.Session, headers: dict = None) -> dict:
    """ Function which returns a dict of champs & their corresponding runeforge links """
    soup = BeautifulSoup(session.get('http://runeforge.gg/', headers=headers).text, 'lxml')

    # Champs with only a single runepage
    single_champs_raw = soup.find_all('li', class_='champion')
    single_champs = {x.a.div.div['style'][77:-6].lower(): [x.a['href']] for x in single_champs_raw if
                     x.a is not None}

    # Champs with two (or more) runepages
    double_champs_raw = soup.find_all('div', class_='champion-modal-open')
    double_champs_decode = [json.loads(x['data-loadouts']) for x in double_champs_raw]
    double_champs = {x[0]['champion'].lower(): [x[0]['link'], x[1]['link']] for x in double_champs_decode}

    champs_combined = {**single_champs, **double_champs}

    return champs_combined


def parse_rune_html(html: str) -> dict:
    """ A function which returns a dict representation of the Runeforge.gg web page """
    soup = BeautifulSoup(html, 'lxml')
    champ = soup.find('h1', class_='champion-header--title').text
    title = soup.find('h2', class_='loadout-title').text
    description = soup.find('p').text
    p_tree, s_tree = [x.text for x in soup.find_all('h2', class_='rune-path--name')]
    all_runes = soup.find_all('a', class_='rune-name')
    keystone = all_runes[0].text
    p_rest = [x.text for x in all_runes[1:4]]
    s_rest = [x.text for x in all_runes[4:7]]

    return {'name': champ, 'title': title, 'description': description,
            'runes': {'primary': {'name': p_tree, 'keystone': keystone, 'rest': p_rest},
                      'secondary': {'name': s_tree, 'rest': s_rest}}}
