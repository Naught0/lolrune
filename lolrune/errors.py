class LoLRuneException(Exception):
    """Base exception for library exceptions.
    """
    pass


class RuneConnectionError(LoLRuneException):
    """Raised when a request does not have a status of 200.

    Parameters
    ----------
    status : int
        The status of the request which failed.
    """

    def __init__(self, status):
        self.message = 'Runeforge.gg failed to respond with status {}.'.format(status)


class ChampNotFoundError(LoLRuneException):
    """Raised when a champion is not found in the ``rune_links``.

    Parameters
    ----------
    champ : str
        The champion which was not found.
    """

    def __init__(self, champ):
        self.message = 'No champs matching {}'.format(champ)
        super().__init__(self.message)
