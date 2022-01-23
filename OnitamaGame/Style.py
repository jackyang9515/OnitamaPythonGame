from __future__ import annotations
from typing import List, Tuple, Union
from Pieces import Pieces


class Style:
    """
    Style is the movement pattern used in the game Onitama. In our
    implementation, there are 5 styles in total, they are crab, horse, mantis,
    rooster and dragon.

    Attributes:

    name: name of the style
    owner: the current user of this particular style

    Private Attributes:

    _moves: the list that contains the move patterns
    """
    name: str
    _moves: List[Tuple[int, int]]
    owner: str

    def __init__(self, pairs: List[Tuple[int, int]], name: str,
                 owner: str = Pieces.EMPTY) -> None:
        """
        Constructs a style with a name, an owner and an organized moving
        directory
        """
        self.name = name
        self._moves = pairs.copy()
        self.owner = owner

    def get_moves(self) -> List[Tuple[int, int]]:
        """
        Returns a deep copy of the move patterns (self._moves)
        """
        return self._moves.copy()

    def __eq__(self, other: Style) -> bool:
        """
        Overrides default "==". Returns true iff two styles are being
        compared and their names and owners are the same
        """
        return self.name == other.name and self.owner == other.owner

    def __copy__(self) -> Style:
        """
        Overrides default shallow copy and instead pass in the deep copy of
        the _moves attribute
        """
        return Style(self._moves.copy(), self.name, self.owner)
