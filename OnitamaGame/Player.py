from __future__ import annotations
from Pieces import Pieces
from Style import Style
from typing import Dict, List, Tuple, Union
from Turn import Turn
from random import randint


class Player:
    """
    The class that represents the two players of the game.

    Attributes:

    player_id: the name of the player
    onitama: the onitama game itself
    """
    player_id: str

    def __init__(self, player_id: str) -> None:
        """
        Initializes the player class
        """
        self.player_id = player_id

    def get_turn(self) -> Union[None, Turn]:
        """
        The base method of get_turn. Get a turn out of possible turns.
        Must be implemented by subclasses
        """
        raise NotImplementedError

    def get_tokens(self) -> List[Tuple[int, int]]:
        """
        Get all the chess pieces on the board that belongs to the player
        """
        board = self.onitama.get_board()
        tokens = []
        for i, row in enumerate(board):
            for j, token in enumerate(row):
                if token.lower() == self.player_id.lower():
                    tokens.append((i, j))
        return tokens

    def get_styles(self) -> List[Style]:
        """
        Get the list of styles that can be currently used by the player
        """
        styles = []
        for sty in self.onitama.get_styles():
            if sty.owner == self.player_id:
                styles.append(sty)
        return styles

    def get_valid_turns(self) -> Dict[str, List[Turn]]:
        """
        Creates a dictionary that stores all the possible valid moves of the
        current player
        """
        styles = self.get_styles()
        tokens = self.get_tokens()
        turns = {}
        for sty in styles:
            turns[sty.name] = []
            for row, col in tokens:
                for d_row, d_col in sty.get_moves():
                    # Flip move direction if player is X
                    if self.player_id == Pieces.G1:
                        d_row *= -1
                        d_col *= -1
                    # Check is_legal_move
                    if self.onitama.is_legal_move(row, col, row + d_row, col + d_col):
                        turns[sty.name].append(Turn(row, col, row + d_row,
                                                    col + d_col, sty.name, self.player_id))

        return turns

    def set_onitama(self, onitama) -> None:
        """
        Set the OnitamaGame as one of the attributes
        """
        self.onitama = onitama


class PlayerRandom(Player):
    """
    The subclass of the class Player. Basically a player who plays randomly
    """

    def __init__(self, player_id: str) -> None:
        """
        Initializes the PLayerRandom class
        """
        super().__init__(player_id)

    def get_turn(self) -> Union[None, Turn]:
        """
        Get a random turn out of the result of get_valid_turns()
        """
        turns = []
        valid_turns = self.get_valid_turns()
        for style_name in valid_turns:
            turns.extend(valid_turns[style_name])

        # Return a random valid turn
        if len(turns) == 0:
            return None
        return turns[randint(0, len(turns) - 1)]
