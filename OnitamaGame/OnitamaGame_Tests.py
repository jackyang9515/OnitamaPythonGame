"""
This file contains the pytests of the file OnitamaGame.py
"""

from OnitamaGame import OnitamaGame
from Player import Player
from Pieces import Pieces

from hypothesis import given
from hypothesis.strategies import integers

import pytest


# other_player


def test_other_player() -> None:
    """
    Test whether if other_player works. There are four test cases:
    player1, player2, player1 twice and invalid player
    """
    game = OnitamaGame(5, Player('p1'), Player('p2'))
    assert game.other_player(game.player1) == game.player2
    assert game.other_player(game.player2) == game.player1
    assert game.other_player(game.other_player(game.player1)) == game.player1
    assert game.other_player(Player('popo')) is None


# get_token

@given(integers(0, 55), integers(), integers(5, 55))
def test_get_token(n1: int, n2: int, n3: int) -> None:
    """
    Test if get_token works or not. Raise error if it malfunctions on
    a new board.
    """
    if n3 % 2 == 1:
        game = OnitamaGame(n3, Player('p1'), Player('p2'))
        if 0 == n1 and (n3 - 1) >= n2 >= 0 and n2 != n3 // 2:
            assert game.get_token(n1, n2) == 'x'
        elif 0 == n1 and (n3 - 1) >= n2 >= 0 and n2 == n3 // 2:
            assert game.get_token(n1, n2) == 'X'
        elif (n3 - 1) == n1 and (n3 - 1) >= n2 >= 0 and n2 != n3 // 2:
            assert game.get_token(n1, n2) == 'y'
        elif (n3 - 1) == n1 and (n3 - 1) >= n2 >= 0 and n2 == n3 // 2:
            assert game.get_token(n1, n2) == 'Y'
        else:
            assert game.get_token(n1, n2) == ' '


def test_get_token_aftermove() -> None:
    """
    See if get_token works after moving a chess piece.
    """
    game = OnitamaGame(5, Player('p1'), Player('p2'))
    assert game.move(0, 0, 1, 0, 'crab') is True
    assert game.get_token(1, 0) == Pieces.M1


# is_legal_move

@given(integers(0, 4), integers(0, 4), integers(), integers())
def test_is_legal_move_player1(n1: int, n2: int, n3: int, n4: int) -> None:
    """
    Tests whether is_legal_move works or not. This function tests for all three
    conditions: starts from a valid point, destination within board and the
    fact that you can't move on top of your own piece.
    """
    game = OnitamaGame(5, Player('p1'), Player('p2'))
    if n1 != 0:  # has to start from a valid point
        assert game.is_legal_move(n1, n2, n3, n4) is False
    elif n3 < 0 or n4 < 0 or n3 > 4 or n4 > 4:  # destination within board
        assert game.is_legal_move(n1, n2, n3, n4) is False
    elif n3 == 0 and 0 <= n4 <= 4:  # can't move on to your on piece
        assert game.is_legal_move(n1, n2, n3, n4) is False
    else:
        assert game.is_legal_move(n1, n2, n3, n4) is True


@given(integers(0, 4), integers(0, 4), integers(), integers())
def test_is_legal_move_player2(n1: int, n2: int, n3: int, n4: int) -> None:
    """
    Same as the function for player1, except it's for player 2 this time.
    """
    game = OnitamaGame(5, Player('p1'), Player('p2'))
    game.whose_turn = game.player2
    if n1 != 4:  # has to start from a valid point
        assert game.is_legal_move(n1, n2, n3, n4) is False
    elif n3 < 0 or n4 < 0 or n3 > 4 or n4 > 4:  # destination within board
        assert game.is_legal_move(n1, n2, n3, n4) is False
    elif n3 == 4 and 0 <= n4 <= 4:  # can't move on to your on piece
        assert game.is_legal_move(n1, n2, n3, n4) is False
    else:
        assert game.is_legal_move(n1, n2, n3, n4) is True


def test_invalid_player_legalmove() -> None:
    """
    Tries to move the chess piece of player 1 during player2's turn. It is going
    to return false
    """
    game = OnitamaGame(5, Player('p1'), Player('p2'))
    game.whose_turn = game.player2

    # Normally this works, but we have player2 occupying the current turn,
    # so our fxn returns false instead.
    assert game.is_legal_move(0, 0, 1, 0) is False


# move


def test_move_on_style() -> None:
    """
    A test trying to break move(). Exact steps explained below.
    """
    game = OnitamaGame(5, Player('p1'), Player('p2'))

    # player tries to use the style he doesn't have

    assert game.move(0, 0, 1, 1, 'mantis') is False
    assert game.move(0, 2, 1, 0, 'dragon') is False

    # player's movement doesn't follow the style

    assert game.move(0, 0, 4, 0, 'crab') is False
    assert game.move(0, 4, 4, 4, 'horse') is False


def test_move_on_coords() -> None:
    """
    A test trying to break move(). Exact steps explained below.
    """
    game = OnitamaGame(5, Player('p1'), Player('p2'))

    # player tries to move outside of board

    assert game.move(0, 0, -1, 0, 'horse') is False
    game.whose_turn = game.player2
    assert game.move(4, 0, 5, 0, 'mantis') is False

    # player tries to move empty/chess pieces that doesn't belong to them
    assert game.move(1, 0, 0, 1, 'mantis') is False
    game.whose_turn = game.player1
    assert game.move(2, 2, 3, 2, 'horse') is False

    assert game.move(4, 2, 3, 2, 'horse') is False
    game.whose_turn = game.player2
    assert game.move(0, 1, 1, 1, 'mantis') is False


def test_valid_moves() -> None:
    """
    This functions tests whether move() actually moves the chess pieces or not.
    """
    game = OnitamaGame(5, Player('p1'), Player('p2'))
    assert game.move(0, 4, 1, 4, 'horse') is True
    assert game.get_token(1, 4) == 'x'
    assert game.whose_turn == game.player2
    assert game.get_styles()[1].owner == ' '
    assert game.get_styles()[4].owner == 'p1'

    assert game.move(4, 4, 3, 3, 'mantis') is True
    assert game.get_token(3, 3) == 'y'
    assert game.whose_turn == game.player1
    assert game.get_styles()[2].owner == ' '
    assert game.get_styles()[1].owner == 'p2'

    assert game.move(1, 4, 1, 2, 'crab') is True
    assert game.get_token(1, 2) == 'x'
    assert game.whose_turn == game.player2
    assert game.get_styles()[0].owner == ' '
    assert game.get_styles()[2].owner == 'p1'


# get_winner

@given(integers(5, 55))
def test_no_master_onboard(n1: int) -> None:
    """
    This function tests for get_winner, and have provided three conditions of
    the board. 0, 1 or 2 masters onboard.
    """
    if n1 % 2 == 1:
        game = OnitamaGame(n1, Player('p1'), Player('p2'))

        # no master on board

        game.set_token(0, game.size // 2, Pieces.EMPTY)
        game.set_token(game.size - 1, game.size // 2, Pieces.EMPTY)
        assert game.get_winner() is None

        # one master on board

        game.set_token(0, 0, Pieces.G2)
        assert game.get_winner() == game.player2
        game.set_token(0, 0, Pieces.G1)
        assert game.get_winner() == game.player1

        # two masters on board

        game.set_token(0, 1, Pieces.G2)
        assert game.get_winner() is None


@given(integers(5, 55))
def test_starting_positions(n1: int) -> None:
    """
    This function tests for get_winner, and the steps are explained below.
    """
    if n1 % 2 == 1:
        game = OnitamaGame(n1, Player('p1'), Player('p2'))

        # p1 captures p2's starting position

        game.set_token(0, 0, Pieces.G2)
        game.set_token(0, game.size // 2, Pieces.EMPTY)
        game.set_token(game.size - 1, game.size // 2, Pieces.G1)
        assert game.get_winner() == game.player1

        # p2 captures p1's starting position

        game.set_token(game.size - 1, game.size // 2, Pieces.EMPTY)
        game.set_token(1, 0, Pieces.G1)
        game.set_token(0, game.size // 2, Pieces.G2)
        assert game.get_winner() == game.player2

        # both masters are on each other's starting positions. This is
        # not likely to happen in the game, but it's a possibility with this fxn

        game.set_token(game.size - 1, game.size // 2, Pieces.G1)
        assert game.get_winner() is None


def test_move_to_victory() -> None:
    """
    Get a winner from the beginning. The winner is player2.
    """
    game = OnitamaGame(5, Player('p1'), Player('p2'))
    assert game.move(0, 2, 1, 2, 'crab') is True
    assert game.move(4, 2, 3, 1, 'mantis') is True
    assert game.move(1, 2, 2, 2, 'horse') is True
    assert game.move(3, 1, 2, 2, 'rooster') is True
    assert game.get_winner() == game.player2


# undo


def test_one_move_undo() -> None:
    """
    Undo one move.
    """
    game = OnitamaGame(5, Player('p1'), Player('p2'))
    assert game.move(0, 0, 1, 0, 'horse') is True
    game.undo()
    assert game.get_token(0, 0) == 'x'
    assert game.get_styles()[1].owner == 'p1'


def test_two_moves_undo() -> None:
    """
    Undo two moves.
    """
    game = OnitamaGame(5, Player('p1'), Player('p2'))
    assert game.move(0, 4, 1, 4, 'crab') is True
    assert game.move(4, 0, 3, 1, 'mantis') is True
    game.undo()
    assert game.get_token(1, 4) == 'x'
    assert game.get_styles()[0].owner == ' '
    assert game.get_styles()[2].owner == 'p2'


def test_undo_after_victory() -> None:
    """
    Undo after a player wins the game.
    """
    game = OnitamaGame(5, Player('p1'), Player('p2'))
    assert game.move(0, 2, 1, 2, 'crab') is True
    assert game.move(4, 2, 3, 1, 'mantis') is True
    assert game.move(1, 2, 2, 2, 'horse') is True
    assert game.move(3, 1, 2, 2, 'rooster') is True
    assert game.get_winner() == game.player2
    game.undo()
    assert game.get_winner() is None


def test_no_move_undo() -> None:
    """
    Undo right after the game launches. Nothing is suppose to happen.
    """
    game = OnitamaGame(5, Player('p1'), Player('p2'))
    game_board = game.get_board()
    game_styles = game.get_styles_deep_copy()
    game.undo()
    assert game.get_board() == game_board
    assert game.get_styles() == game_styles


if __name__ in '__main__':

    pytest.main(['OnitamaGame_Tests.py'])
