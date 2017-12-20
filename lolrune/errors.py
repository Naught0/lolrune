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
        self.message = f'Runeforge.gg failed to respond with status {status}.'


class ChampNotFoundError(LoLRuneException):
    """Raised when a champion is not found in the .data/rune_links.json file.

    Parameters
    ----------
    champ : str
        The champion which was not found.
    """

    def __init__(self, champ):
        self.message = f'No champs matching {champ}.'
        super().__init__(self.message)
