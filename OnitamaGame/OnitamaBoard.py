from Player import Player
from typing import List, Union
from Style import Style
from Pieces import Pieces
from StyleImages import StyleImages


class EvenNumberSizeError(Exception):

    def __str__(self) -> str:
        return 'you have entered a even number for size'


class InvalidBoardError(Exception):
    pass


class OnitamaBoard:
    """
    An OnitamaBoard class consisting of a game board, and keeping track of player token information and styles.
    It can set and clear the board and check if potential plays are valid through coordinate checking.

    === Attributes ===
    size : A board's width and height.
    player1 : Player object representing player who will play the G1 and M1 pieces.
    player2 : Player object representing player who will play the G2 and M2 pieces.
    styles :  A list of all possible play styles including: dragon, crab, horse, mantis, rooster.

    === Private Attributes ===
    _board :
        A nested list representing a grid layout for the board.

    === Representation Invariants ===
    - Size is always an odd number greater or equal to 5.
    - player1 has G1 and M1 pieces.
    - player2 has G2 and M2 pieces.
    """
    size: int
    player1: Player
    player2: Player
    styles: List[Style]
    _board: List[List[str]]

    def __init__(self, size: int, player1: Player, player2: Player,
                 board: Union[List[List[str]], None] = None) -> None:
        """
        Constructs an empty Onitama board. Places four monks and one grandmaster
        on opposite sides of the board. Creates five Styles and distributes them
        among the players.

        """
        # TODO: Your code goes here
        if size >= 5 and size % 2 != 0:
            self.size = size
        else:
            raise EvenNumberSizeError
        self.player1 = player1
        self.player2 = player2
        if board is not None:
            if self._list_size_correct(size, board):
                self._board = [row.copy() for row in board]
            else:
                raise InvalidBoardError
        else:
            self._board = self.board_construct_help()
        self.construct_styles()

    def _list_size_correct(self, size: int, board: List[List[str]]) -> bool:
        if len(board) != size:
            return False
        counter = True
        for lst in board:
            if len(lst) != size:
                counter = False
        return counter

    def board_construct_help(self) -> List[List[str]]:
        master_spot = self.size // 2
        new_list = []
        while not len(new_list) == self.size:
            new_list.append([])
        for lst in new_list[1:self.size - 1]:
            while len(lst) < self.size:
                lst.append(Pieces.EMPTY)

        while not len(new_list[0]) == self.size:
            new_list[0].append(Pieces.M1)
        new_list[0][master_spot] = Pieces.G1

        while not len(new_list[self.size - 1]) == self.size:
            new_list[self.size - 1].append(Pieces.M2)
        new_list[self.size - 1][master_spot] = Pieces.G2
        return new_list

    def construct_styles(self) -> None:
        """
        Constructs the 5 movement styles of Onitama for this board. Normally,
        there are 16 movement styles and they are distributed randomly, however for
        this assignment, you are only required to use 5 of them (Dragon, Crab, Horse,
        Mantis, and Rooster).

        You can find the movement patterns for these styles under assets/{style}.png,
        where {style} is one of the five styles mentioned above. Additionally, you
        can also find the images in README.md.

        IMPORTANT: Additionally, we are going to distribute the styles at the start
        of the game in a static or consistent manner. Player 1 (G1) must get the Crab
        and Horse styles. Player 2 (G2) must get the Mantis and Rooster styles. Extra
        (EMPTY) must get the Dragon style.

        Please be sure to follow the distribution of styles as mentioned above as
        this is important for testing. Failure to follow this distribution of styles
        will result in the LOSS OF A LOT OF MARKS.

        The first list is for p1, which is michael, and second list is for ilir
        the second player

        >>> board = OnitamaBoard(5, Player('p1'), Player('p2'))
        >>> print(board.styles[0].get_moves())
        [(0, -2), (0, 2), (-1, 0)]
        >>> print(board.styles[1].owner)
        p1
        >>> print(board.styles[4].owner)
        <BLANKLINE>
        """
        # TODO: Your code goes here
        crab_style = Style([(0, -2), (0, 2), (-1, 0)],
                           StyleImages.CRAB, self.player1.player_id)
        horse_style = Style([(1, 0), (0, -1), (-1, 0)],
                            StyleImages.HORSE, self.player1.player_id)
        mantis_style = Style([(-1, -1), (-1, 1), (1, 0)],
                             StyleImages.MANTIS, self.player2.player_id)
        rooster_style = Style([(-1, 1), (0, 1), (0, -1), (1, -1)],
                              StyleImages.ROOSTER, self.player2.player_id)
        dragon_style = Style([(-1, -2), (-1, 2), (1, -1), (1, 1)],
                             StyleImages.DRAGON)
        self.styles = [crab_style, horse_style,
                       mantis_style, rooster_style, dragon_style]

    def exchange_style(self, style: Style) -> bool:
        """
        Exchange the given <style> with the empty style (the style whose owner is
        EMPTY). Hint: Exchanging will involve swapping the owners of the styles.

        Precondition: <style> cannot be the empty style.

        >>> board = OnitamaBoard(5, Player('p1'), Player('p2'))
        >>> board.exchange_style(board.styles[0])
        True
        >>> print(board.styles[0].owner)
        <BLANKLINE>
        >>> print(board.styles[4].owner)
        p1
        >>> board.exchange_style(board.styles[2])
        True
        >>> print(board.styles[2].owner)
        <BLANKLINE>
        >>> print(board.styles[0].owner)
        p2
        >>> board.exchange_style(board.styles[2])
        False
        """
        # TODO: Your code goes here
        if style.owner == Pieces.EMPTY:
            return False
        else:
            for sty in self.styles:
                if sty.owner == Pieces.EMPTY:
                    sty.owner, style.owner = style.owner, Pieces.EMPTY
            return True

    def valid_coordinate(self, row: int, col: int) -> bool:
        """
        Returns true iff the provided coordinates are valid (exists on the board).

        >>> board = OnitamaBoard(5, Player('p1'), Player('p2'))
        >>> board.valid_coordinate(0, 0)
        True
        >>> board.valid_coordinate(2, 3)
        True
        >>> board.valid_coordinate(5, 0)
        False
        """
        if self.size > row >= 0 and 0 <= col < self.size:
            return True
        else:
            return False

    def get_token(self, row: int, col: int) -> str:
        """
        Returns the player token that is in the given <row> <col> position, or the empty
        character if no player token is there or if the position provided is invalid.

        >>> board = OnitamaBoard(5, Player('p1'), Player('p2'))
        >>> board.get_token(0, board.size // 2)
        'X'
        >>> board.get_token(2, 3)
        ' '
        >>> board.get_token(5, 5)
        ' '
        """
        # TODO: Your code goes here
        if 0 <= row < self.size and 0 <= col < self.size:
            return self._board[row][col]
        else:
            return Pieces.EMPTY

    def set_token(self, row: int, col: int, token: str) -> None:
        """
        Sets the given position on the board to be the given player (or throne/empty)
        <token>.

        Precondition: row and col must be in the board

        >>> board = OnitamaBoard(5, Player('p1'), Player('p2'))
        >>> board.set_token(0, 0, Pieces.G1)
        >>> board.get_token(0, 0)
        'X'
        >>> board.set_token(2, 3, Pieces.M1)
        >>> board.get_token(2, 3)
        'x'
        >>> board.set_token(5, 5, Pieces.M1)
        >>> board.get_token(5, 5)
        ' '
        """
        # TODO: Your code goes here
        if self.valid_coordinate(row, col):
            self._board[row][col] = token

    def get_styles_deep_copy(self) -> List[Style]:
        """
        DO NOT MODIFY THIS!!!
        Returns a deep copy of the styles of this board.
        """
        return [style.__copy__() for style in self.styles]

    def deep_copy(self) -> List[List[str]]:
        """
        DO NOT MODIFY THIS!!!
        Creates and returns a deep copy of this OnitamaBoard's
        current state.
        """
        return [row.copy() for row in self._board]

    def set_board(self, board: List[List[str]]) -> None:
        """
        DO NOT MODIFY THIS!!!
        Sets the current board's state to the state of the board which is passed in as a parameter.
        """
        self._board = [row.copy() for row in board]


if __name__ in '__main__':
    import doctest

    doctest.testmod()
