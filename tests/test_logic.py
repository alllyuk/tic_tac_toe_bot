from src.game.board import Board
from src.game.logic import GameLogic


def test_check_winner_horizontal():
    board = Board.create_empty()
    # Заполняем первую строку крестиками
    board.state[0] = [Board.CROSS, Board.CROSS, Board.CROSS]
    assert GameLogic.check_winner(board)


def test_check_winner_vertical():
    board = Board.create_empty()
    # Заполняем первый столбец нуликами
    for i in range(3):
        board.state[i][0] = Board.ZERO
    assert GameLogic.check_winner(board)


def test_check_winner_diagonal():
    board = Board.create_empty()
    # Заполняем главную диагональ крестиками
    for i in range(3):
        board.state[i][i] = Board.CROSS
    assert GameLogic.check_winner(board)


def test_bot_move():
    board = Board.create_empty()
    row, col = GameLogic.make_bot_move(board)
    assert 0 <= row <= 2
    assert 0 <= col <= 2
    assert board.is_cell_free(row, col)
