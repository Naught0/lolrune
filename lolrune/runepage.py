from collections import namedtuple
from typing import NamedTuple, List


Tree = NamedTuple('Tree', [('name', str), ('runes', List[str])])
"""A :func:`namedtuple <collections.namedtuple>` which represents a specific tree in a :class:`RunePage`.

Attributes
----------
name : str
    The name of the rune tree, e.g. ``'Precision'``.

runes : List[str]
    A list of runes in a page, e.g.:
    
    .. code:: python3

        ['Cheap Shot', 'Ghost Poro', 'Relentless Hunter']
"""


class Champion:
    """Represents a champion and contains that champ's rune page.

    Parameters
    ----------
    rune_data : dict
        The entirety of the rune page data returned by :meth:`~lolrune.RuneClient.get_runes`.

    Attributes
    ----------
    name : str
        The champion's name e.g. ``'Kalista'``.

    title : str
        The title assigned to the particular champion's rune page by runeforge.gg.
        This is largely meaningless, e.g. ``'Bloodshed Carries a Price'``.

    description : str
        A slightly less meaningless description of the rune page e.g., 
        ``'Lethality focused long range poke with [Q].'``.

    runes : :class:`RunePage`
        Contains rune information.
    """
    def __init__(self, rune_data: dict):
        self.name = rune_data['name']
        self.title = rune_data['title']
        self.description = rune_data['description']
        self.runes = RunePage(rune_data['runes'])


class RunePage:
    """An object representing a specific rune page for a :class:`~lolrune.Champion`.

    Parameters
    ----------
    rune_page : dict
        The nested data contained in ``rune_data['runes']``.

    Attributes
    ----------
    keystone : str
        The keystone for the page, e.g. ``'Arcane Comet'``.

    primary : :obj:`Tree`
        A representation of the primary rune tree.

    secondary : :obj:`Tree`
        A representation of the secondary rune tree.

        Example
        -------
        .. code:: python3

            >>> from lolrune import RuneClient
            >>> client = RuneClient()
            >>> champ = client.get_runes('bard')[0]

            >>> print(champ.name)
            Bard
            >>> print('{}: {}'.format(champ.title, champ.description))
            Gimmie All Those Chimes: Map Roaming and kill pressure.
            >>> print(champ.runes.keystone)
            Electrocute
            >>> print(champ.runes.primary)
            Tree(name='Domination', runes=['Cheap Shot', 'Zombie Ward', 'Relentless Hunter'])
            >>> print('{}: {}'.format(champ.runes.primary.name, ', '.join(champ.runes.primary.runes)))
            Domination: Cheap Shot, Zombie Ward, Relentless Hunter
            >>> print('{}: {}'.format(champ.runes.secondary.name, ', '.join(champ.runes.secondary.runes)))
            Sorcery: Scorch, Manaflow Band
    """
    TREE = namedtuple('Tree', 'name runes')
    def __init__(self, rune_page: dict):
        self.__dict__.update(rune_page)
        self.keystone = rune_page['primary']['keystone']
        self.primary = self.TREE(name=rune_page['primary']['name'], runes=rune_page['primary']['rest'])
        self.secondary = self.TREE(name=rune_page['secondary']['name'], runes=rune_page['secondary']['rest'])
