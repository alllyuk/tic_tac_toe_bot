from random import choice
from .board import Board


class GameLogic:
    @staticmethod
    def check_winner(board: Board) -> bool:
        state = board.state

        for i in range(3):
            if (
                state[i][0] == state[i][1] == state[i][2] != board.FREE_SPACE
                or
                state[0][i] == state[1][i] == state[2][i] != board.FREE_SPACE
                ):
                return True

        if (
            state[0][0] == state[1][1] == state[2][2] != board.FREE_SPACE
            or
            state[0][2] == state[1][1] == state[2][0] != board.FREE_SPACE
            ):
            return True

        return False

    @staticmethod
    def make_bot_move(board: Board) -> tuple[int, int]:
        free_cells = board.get_free_cells()
        return choice(free_cells) if free_cells else (-1, -1)
