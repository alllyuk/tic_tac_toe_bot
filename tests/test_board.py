from src.game.board import Board


def test_create_empty_board():
    board = Board.create_empty()
    assert all(cell == Board.FREE_SPACE for row in board.state for cell in row)


def test_is_cell_free():
    board = Board.create_empty()
    assert board.is_cell_free(0, 0)
    board.state[0][0] = Board.CROSS
    assert not board.is_cell_free(0, 0)
