class LoLRuneException(Exception):
    """ Base exception for library exceptions """
    pass


class RuneConnectionError(LoLRuneException):
    """ Raised when the requests status indicates a problem """

    def __init__(self, status):
        self.message = f'Runeforge.gg failed to respond with status {status}.'


class ChampNotFoundError(LoLRuneException):
    """ Raised when champion input is invalid """

    def __init__(self, champ):
        self.message = f'No champs matching {champ}.'
        super().__init__(self.message)
