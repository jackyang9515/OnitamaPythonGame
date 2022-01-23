from OnitamaBoard import OnitamaBoard
from Player import Player
from Pieces import Pieces

from hypothesis import given
from hypothesis.strategies import integers

import pytest

# construct_styles


def test_for_style_moves() -> None:
    """
    Checks whether construct_styles have the right movements or not.
    """
    board = OnitamaBoard(5, Player('p1'), Player('p2'))
    all_move_lst = []
    for sty in board.styles:
        all_move_lst.append(sty.get_moves())
    assert all_move_lst == [[(0, -2), (0, 2), (-1, 0)],
                            [(1, 0), (0, -1), (-1, 0)],
                            [(-1, -1), (-1, 1), (1, 0)],
                            [(-1, 1), (0, 1), (0, -1), (1, -1)],
                            [(-1, -2), (-1, 2), (1, -1), (1, 1)]]


def test_for_style_names() -> None:
    """
    Checks whether construct_styles have the right style names or not.
    """
    board = OnitamaBoard(5, Player('p1'), Player('p2'))
    all_name_lst = []
    for sty in board.styles:
        all_name_lst.append(sty.name)
    assert all_name_lst == ['crab', 'horse', 'mantis', 'rooster', 'dragon']


def test_for_style_owners() -> None:
    """
    Checks whether construct_styles have the right style owners or not.
    """
    board = OnitamaBoard(5, Player('p1'), Player('p2'))
    all_owner_lst = []
    for sty in board.styles:
        all_owner_lst.append(sty.owner)
    assert all_owner_lst == ['p1', 'p1', 'p2', 'p2', Pieces.EMPTY]


# exchange_style

@given(integers(0, 4))
def test_exchange_all_styles(n1: int) -> None:
    """
    Exchanges the styles. Raises error if empty style is being
    exchanged as main.
    """
    board = OnitamaBoard(5, Player('p1'), Player('p2'))
    if 3 >= n1 >= 0:
        result = board.exchange_style(board.styles[n1])
        assert result is True
        assert board.styles[n1].owner == Pieces.EMPTY
    else:
        result = board.exchange_style(board.styles[n1])
        assert result is False
        assert board.styles[n1].owner == Pieces.EMPTY


# valid_coordinate

@given(integers(), integers(), integers(5, 55))
def test_verify_all_coordinates(n1: int, n2: int, n3: int) -> None:
    """
    Test for valid_coordinate. Works for boards bigger than 5 as well.
    """
    if n3 % 2 == 1:
        board = OnitamaBoard(n3, Player('p1'), Player('p2'))
        if (n3 - 1) >= n1 >= 0 and (n3 - 1) >= n2 >= 0:
            assert board.valid_coordinate(n1, n2) is True
        else:
            assert board.valid_coordinate(n1, n2) is False


# get_token

@given(integers(0, 55), integers(), integers(5, 55))
def test_get_all_tokens(n1: int, n2: int, n3: int) -> None:
    """
    Test for get_token. Works for boards bigger than 5 as well.
    """
    if n3 % 2 == 1:
        board = OnitamaBoard(n3, Player('p1'), Player('p2'))
        if 0 == n1 and (n3 - 1) >= n2 >= 0 and n2 != n3 // 2:
            assert board.get_token(n1, n2) == 'x'
        elif 0 == n1 and (n3 - 1) >= n2 >= 0 and n2 == n3 // 2:
            assert board.get_token(n1, n2) == 'X'
        elif (n3 - 1) == n1 and (n3 - 1) >= n2 >= 0 and n2 != n3 // 2:
            assert board.get_token(n1, n2) == 'y'
        elif (n3 - 1) == n1 and (n3 - 1) >= n2 >= 0 and n2 == n3 // 2:
            assert board.get_token(n1, n2) == 'Y'
        else:
            assert board.get_token(n1, n2) == ' '


# set_token

@given(integers(), integers(), integers(5, 55))
def test_set_g1(n1: int, n2: int, n3: int) -> None:
    """
    Test for set_token. Set the chosen coord as grand master1.
    """
    if n3 % 2 == 1:
        board = OnitamaBoard(n3, Player('p1'), Player('p2'))
        board.set_token(n1, n2, Pieces.G1)
        if board.valid_coordinate(n1, n2):
            assert board.get_token(n1, n2) == 'X'


@given(integers(), integers(), integers(5, 55))
def test_set_m1(n1: int, n2: int, n3: int) -> None:
    """
    Test for set_token. Set the chosen coord as monk1.
    """
    if n3 % 2 == 1:
        board = OnitamaBoard(n3, Player('p1'), Player('p2'))
        board.set_token(n1, n2, Pieces.M1)
        if board.valid_coordinate(n1, n2):
            assert board.get_token(n1, n2) == 'x'


@given(integers(), integers(), integers(5, 55))
def test_set_g2(n1: int, n2: int, n3: int) -> None:
    """
    Test for set_token. Set the chosen coord as grand master2.
    """
    if n3 % 2 == 1:
        board = OnitamaBoard(n3, Player('p1'), Player('p2'))
        board.set_token(n1, n2, Pieces.G2)
        if board.valid_coordinate(n1, n2):
            assert board.get_token(n1, n2) == 'Y'


@given(integers(), integers(), integers(5, 55))
def test_set_m2(n1: int, n2: int, n3: int) -> None:
    """
    Test for set_token. Set the chosen coord as monk2.
    """
    if n3 % 2 == 1:
        board = OnitamaBoard(n3, Player('p1'), Player('p2'))
        board.set_token(n1, n2, Pieces.M2)
        if board.valid_coordinate(n1, n2):
            assert board.get_token(n1, n2) == 'y'


if __name__ == '__main__':

    pytest.main(['OnitamaBoard_Tests.py'])
