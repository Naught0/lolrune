from collections import namedtuple

TREE = namedtuple('Tree', 'name runes')


class Champion:
    """Represents a champion and contains that champ's rune page.

    Parameters
    ----------
    rune_data : dict
        The entirety of the rune page data returned by :meth:`~lolrune.RuneClient.get_runes`.

    Attributes
    ----------
        champ_name : str
            The champion's name e.g. ``'Kalista'``.

        title : str
            The title assigned to the particular champion's rune page by runeforge.gg.
            This is largely meaningless, e.g. ``'Bloodshed Carries a Price'``.

        description : str
            A slightly less meaningless description of the rune page.
            For example, ``'Lethality focused long range poke with [Q].'``.

        runes : :class:`~lolrune.RunePage`
            A :class:`<lolrune.RunePage>` object which contains rune information.
    """
    def __init__(self, rune_data: dict):
        self.name = rune_data['name']
        self.title = rune_data['title']
        self.description = rune_data['description']
        self.trees = RunePage(rune_data['runes'])


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

    primary : namedtuple
        A representation of the primary rune tree.

    secondary : namedtuple
        A representation of the secondary rune tree.

        Example
        -------
        .. code:: python3

            from lolrune import RuneClient

            client = RuneClient()
            champ = client.get_runes('bard')[0]

            print(champ.name)
            print('{}: {}'.format(champ.title, champ.description))
            print(champ.trees.keystone)
            print(champ.trees.primary)
            print('{}: {}'.format(champ.trees.primary.name, ', '.join(champ.trees.primary.runes)))
            print('{}: {}'.format(champ.trees.secondary.name, ', '.join(champ.trees.secondary.runes)))

            # Outputs
            Bard
            Gimmie All Those Chimes: Map Roaming and kill pressure.
            Electrocute
            Tree(name='Domination', runes=['Cheap Shot', 'Zombie Ward', 'Relentless Hunter'])
            Domination: Cheap Shot, Zombie Ward, Relentless Hunter
            Sorcery: Scorch, Manaflow Band
    """
    def __init__(self, rune_page: dict):
        self.__dict__.update(rune_page)
        self.keystone = rune_page['primary']['keystone']
        self.primary = TREE(name=rune_page['primary']['name'], runes=rune_page['primary']['rest'])
        self.secondary = TREE(name=rune_page['secondary']['name'], runes=rune_page['secondary']['rest'])
