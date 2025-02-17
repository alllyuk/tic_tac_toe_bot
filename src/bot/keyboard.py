from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from ..game.board import Board


def generate_keyboard(board: Board) -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(
                board.state[r][c],
                callback_data=f'{r}{c}'
            )
            for c in range(3)
        ]
        for r in range(3)
    ]
    return InlineKeyboardMarkup(keyboard)
