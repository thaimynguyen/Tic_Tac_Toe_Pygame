"""Unit testing on main.py file using pytest"""

from main import check_board_full, check_winner


def test_check_board_full():
    assert check_board_full([[1, 0, -1], [0, -1, 1], [1, -1, 0]]) is False
    assert check_board_full([[1, -1, 1], [-1, 1, -1], [1, 1, -1]]) is True


def test_check_winner():
    # Check no winner
    assert check_winner([[1, -1, 1], [1, -1, -1], [-1, 1, 1]]) == None
    # Check horizontal winning line
    assert check_winner([[1, 1, 1], [-1, 0, -1], [-1, 0, 0]]) == "O"
    # Check vertical winning line
    assert check_winner([[0, -1, 0], [1, -1, 0], [1, -1, 1]]) == "X"
    # Check diagonal winning line
    assert check_winner([[1, -1, 0], [1, 1, 0], [-1, -1, 1]]) == "O"
