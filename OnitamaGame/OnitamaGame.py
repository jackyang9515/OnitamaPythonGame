from typing import List, Union
from OnitamaBoard import OnitamaBoard
from Player import Player
from Pieces import Pieces
from OnitamaStack import OnitamaStack
from Style import Style


class OnitamaGame:
    """
    An OnitamaGame class consisting of a game board, and keeping track of which player's
    turn it currently is and some statistics about the game (e.g. how many tokens each player
    has). It knows who the winner of the game is, and when the game is over.

    === Attributes ===
    size : the size of this onitama game.
    player1 : Player object representing player 1(Michael).
    player2 : Player object representing player 2(Ilir).
    whose_turn : Player whose turn it is.
    board_stack : A stack of Onitama boards that

    === Private Attributes ===

    _board:
        Onitama board object with information on player positions and board layout.

    === Representation Invariants ===
    - Size must be an odd number greater or equal to 5

    """
    size: int
    player1: Player
    player2: Player
    _board: OnitamaBoard
    whose_turn: Player
    onitama_stack: OnitamaStack

    def __init__(self, size: int = 5, player1: Union[Player, None] = None,
                 player2: Union[Player, None] = None) -> None:
        """
        DO NOT MODIFY THIS!!!
        Constructs a game of Onitama with 2 players passed in as parameters
        Sets <whose_turn> to <player1>
        Sets the <self.size> of Onitama to the passed in <size> if valid.

        Precondition: The size must be odd and greater than or equal to 5.
        """
        self.size = size
        self.player1 = player1 if player1 is not None else Player(Pieces.G1)
        self.player2 = player2 if player2 is not None else Player(Pieces.G2)
        self.player1.set_onitama(self)
        self.player2.set_onitama(self)
        self._board = OnitamaBoard(self.size, self.player1, self.player2)
        self.whose_turn = self.player1
        self.onitama_stack = OnitamaStack()

    def get_styles(self) -> List[Style]:
        return self._board.styles

    def set_token(self, row: int, col: int, token: str) -> None:
        self._board.set_token(row, col, token)

    def other_player(self, player: Player) -> Union[Player, None]:
        """
        Given one <player>, returns the other player. If the given <player> is invalid,
        returns null.

        >>> game = OnitamaGame(5, Player('p1'), Player('p2'))
        >>> p2 = game.other_player(game.player1)
        >>> p2 == game.player2
        True
        >>> p1 = game.other_player(game.player2)
        >>> p1 == game.player1
        True
        >>> game.other_player(Player('opp'))

        """
        # TODO: Your code goes here
        if player == self.player1:
            return self.player2
        elif player == self.player2:
            return self.player1
        return

    def get_token(self, row: int, col: int) -> str:
        """
        Returns the player token that is in the given position, or the empty
        character if no player token is there or if the position provided is invalid.

        >>> game = OnitamaGame(5, Player('p1'), Player('p2'))
        >>> game.get_token(0, 0)
        'x'
        >>> game.get_token(2, 3)
        ' '
        >>> game.get_token(5, 5)
        ' '
        """
        # TODO: Your code goes here
        return self._board.get_token(row, col)

    def coordinate_within_board(self, row_o: int, col_o: int, row_d: int,
                                col_d: int) -> bool:
        return self._board.valid_coordinate(row_o, col_o) and \
               self._board.valid_coordinate(row_d, col_d)

    def verify_valid_piece(self, row_o: int, col_o: int) -> bool:
        if self._board.get_token(row_o, col_o) in [Pieces.M1, Pieces.G1] \
                and self.whose_turn == self.player1:
            return True
        elif self.get_token(row_o, col_o) in [Pieces.M2, Pieces.G2] \
                and self.whose_turn == self.player2:
            return True
        return False

    def valid_destination(self, row_d: int, col_d: int) -> bool:
        if self.get_token(row_d, col_d) in [Pieces.M1, Pieces.G1] and \
                self.whose_turn == self.player1:
            return False
        elif self._board.get_token(row_d, col_d) in [Pieces.M2, Pieces.G2] and \
                self.whose_turn == self.player2:
            return False
        else:
            return True

    def is_legal_move(self, row_o: int, col_o: int, row_d: int,
                      col_d: int) -> bool:
        """
        Checks if a move with the given parameters would be legal based on the
        origin and destination coordinates.
        This method should specifically check for the following 3 conditions:
            1)  The movement is in the bounds of this game's board.
            2)  The correct piece is being moved based on the current player's turn.
            3)  The destination is valid.
                A player CANNOT move on top of their own piece.

        Precondition: <row_o> and <col_o> must be on the board.

        >>> game = OnitamaGame(5, Player('p1'), Player('p2'))
        >>> game.is_legal_move(0, 0, 0, 1) # This is moving one of the monks on to another friendly monk
        False
        >>> game.is_legal_move(0, 0, 1, 0)
        True
        >>> game.is_legal_move(0, 0, 5, 5) # coords out of bounds
        False
        >>> game.is_legal_move(0, 2, 4, 2)
        True
        """
        # TODO: Your code goes here
        return self.coordinate_within_board(row_o, col_o, row_d, col_d) and \
               self.verify_valid_piece(row_o, col_o) and \
               self.valid_destination(row_d, col_d)

    def follows_correct_style(self, row_o: int, col_o: int,
                              row_d: int, col_d: int, style_name: str) -> bool:
        """
        Checks whether if the provided step follows the provided style.
        Swap the direction for different players

        >>> game = OnitamaGame(5, Player('p1'), Player('p2')) # player1's turn
        >>> game.whose_turn = game.player2
        >>> game.follows_correct_style(4, 2, 3, 3, 'mantis')
        True
        >>> game = OnitamaGame(5, Player('p1'), Player('p2'))
        >>> game.follows_correct_style(0, 0, 1, 1, 'mantis') # p1 doesn't have mantis
        False
        """
        coordinate = (row_d - row_o, col_d - col_o)
        if self.whose_turn == self.player2:
            for sty in self.player2.get_styles():
                if sty.name == style_name and coordinate in sty.get_moves():
                    return True
        elif self.whose_turn == self.player1:
            if coordinate in self.swap_sty_move_p1(style_name):
                return True
        return False

    def swap_sty_move_p1(self, style_name: str) -> List[tuple]:
        """
        >>> game = OnitamaGame(5, Player('p1'), Player('p2'))
        >>> game.swap_sty_move_p1('crab')
        [(0, 2), (0, -2), (1, 0)]
        """
        new_move = []
        for sty in self.player1.get_styles():
            if sty.name == style_name:
                for x, y in sty.get_moves():
                    if x >= 0 and y >= 0:
                        new_move.append((-abs(x), -abs(y)))
                    elif x >= 0 and y < 0:
                        new_move.append((-abs(x), abs(y)))
                    elif x < 0 and y >= 0:
                        new_move.append((abs(x), -abs(y)))
                    elif x < 0 and y < 0:
                        new_move.append((abs(x), abs(y)))
        return new_move

    def move(self, row_o: int, col_o: int, row_d: int, col_d: int,
             style_name: str) -> bool:
        """
        Attempts to make a move for player1 or player2 (depending on whose turn it is) from
        position <row_o>, <col_o> to position <row_d>, <col_d>.

        On a successful move, it stores the current (unmodified) state of the board and
        the list of styles to <self.onitama_stack> by calling the
        <self.onitama_stack.push(var1, var2)> method.

        After storing the move, it will make the valid move and modify the board and
        actually make the move.

        Returns true if the move was successfully made, false otherwise.

        Preconditon: <row_o> and <col_o> must be on the board.

        >>> game = OnitamaGame(5, Player('p1'), Player('p2'))
        >>> game.move(0, 2, 1, 2, 'crab') #####case 1
        True
        >>> game.get_token(1, 2)
        'X'
        >>> game.whose_turn == game.player2
        True
        >>> print(game.get_styles()[0].owner)
        <BLANKLINE>
        >>> print(game.get_styles()[4].owner)
        p1
        >>> game.move(4, 2, 3, 3, 'mantis') #####case2
        True
        >>> game.get_token(3, 3)
        'Y'
        >>> game.whose_turn == game.player1
        True
        >>> print(game.get_styles()[2].owner)
        <BLANKLINE>
        >>> print(game.get_styles()[0].owner)
        p2
        >>> game = OnitamaGame(5, Player('p1'), Player('p2'))
        >>> game.move(0, 1, 1, 1, 'horse') #####case 3
        True
        >>> game.get_token(1, 1)
        'x'
        >>> game.whose_turn == game.player2
        True
        >>> print(game.get_styles()[1].owner)
        <BLANKLINE>
        >>> print(game.get_styles()[4].owner)
        p1
        """
        # TODO: Your code goes here
        if self.is_legal_move(row_o, col_o, row_d, col_d) and self.follows_correct_style(row_o, col_o, row_d, col_d, style_name):
            self.onitama_stack.push((self.get_board(), self.get_styles_deep_copy()))
            for sty in self._board.styles:
                if style_name == sty.name:
                    self._board.exchange_style(sty)
            self._board.set_token(row_d, col_d, self.get_token(row_o, col_o))
            self._board.set_token(row_o, col_o, Pieces.EMPTY)
            self.whose_turn = self.other_player(self.whose_turn)
            return True
        return False

    def starting_pos_captured(self) -> Union[Player, None]:
        if self._board.get_token(0, self.size // 2) == Pieces.G2 and \
                self._board.get_token(self.size - 1, self.size // 2) == Pieces.G1:
            return
        elif self._board.get_token(0, self.size // 2) == Pieces.G2:
            return self.player2
        elif self._board.get_token(self.size - 1, self.size // 2) == Pieces.G1:
            return self.player1
        return

    def no_master_onboard(self) -> Union[Player, None]:
        g1_counter = False
        g2_counter = False
        for row in range(self.size):
            for column in range(self.size):
                if self._board.get_token(row, column) == Pieces.G1:
                    g1_counter = True
                elif self._board.get_token(row, column) == Pieces.G2:
                    g2_counter = True
        if g1_counter is True and g2_counter is False:
            return self.player1
        elif g1_counter is False and g2_counter is True:
            return self.player2
        return None

    def get_winner(self) -> Union[Player, None]:
        """
        Returns the winner of the game if the game is over, or none
        if the game is not yet finished. As per Onitama's rules, the winner of
        the game is the player whose Grandmaster reaches the middle column on the
        opposite row from the start position, OR the player who captures the other
        player's Grandmaster.

        >>> game = OnitamaGame(5, Player('p1'), Player('p2'))
        >>> game.get_winner()

        >>> game._board.set_token(1, game.size // 2, Pieces.G1)
        >>> game._board.set_token(0, game.size // 2, Pieces.G2)
        >>> print(game.get_winner().player_id)
        p2
        >>> game = OnitamaGame(5, Player('p1'), Player('p2'))
        >>> game._board.set_token(0, game.size // 2, Pieces.EMPTY)
        >>> print(game.get_winner().player_id)
        p2
        """
        # TODO: Your code goes here
        if self.starting_pos_captured() is not None:
            return self.starting_pos_captured()
        elif self.no_master_onboard() is not None:
            return self.no_master_onboard()
        return None

    def undo(self) -> None:
        """
        DO NOT MODIFY THIS!!!
        Undo's the Onitama game's state to the previous turn's state if possible.

        >>> game = OnitamaGame(5, Player('p1'), Player('p2'))
        >>> game.move(0, 2, 1, 2, 'crab') #####case 1
        True
        >>> game.undo()
        >>> game.get_token(0, 2)
        'X'
        >>> print(game.get_styles()[0].owner)
        p1
        >>> game = OnitamaGame(5, Player('p1'), Player('p2'))
        >>> game.move(0, 0, 1, 0, 'horse') #####case 2
        True
        >>> game.undo()
        >>> game.get_token(0, 0)
        'x'
        >>> print(game.get_styles()[1].owner)
        p1
        >>> game = OnitamaGame(5, Player('p1'), Player('p2'))
        >>> game.whose_turn = game.player2
        >>> game.move(4, 2, 3, 3, 'mantis') #####case 3
        True
        >>> game.undo()
        >>> game.get_token(4, 2)
        'Y'
        >>> print(game.get_styles()[2].owner)
        p2
        """
        if not self.onitama_stack.empty():
            # The pop call here returns a board and a list of styles that we use
            # to revert to the previous state of the game
            board, styles = self.onitama_stack.pop()
            self._board.set_board(board)
            self._board.styles = styles
            # Switch to the previous player's turn
            self.whose_turn = self.other_player(self.whose_turn)

    def get_styles_deep_copy(self) -> List[Style]:
        """
        DO NOT MODIFY THIS!!!
        Get a DEEP COPY of the different styles of movement in Onitama.
        """
        return self._board.get_styles_deep_copy()

    def get_board(self) -> List[List[str]]:
        """
        DO NOT MODIFY THIS!!!
        Gets a copy of this OnitamaBoard from OnitamaBoard.getBoard()
        """
        return self._board.deep_copy()

    def set_board(self, size: int, board: List[List[str]]) -> None:
        """
        DO NOT MODIFY THIS!!!
        Construct a new OnitamaBoard with the given size and preset board.
        """
        self.size = size
        self._board = OnitamaBoard(
            self.size, self.player1, self.player2, board=board)


if __name__ in '__main__':
    import doctest

    doctest.testmod()
