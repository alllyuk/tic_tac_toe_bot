from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from src.logger import logger

from ..game.board import Board
from ..game.logic import GameLogic
from .keyboard import generate_keyboard

CONTINUE_GAME, FINISH_GAME = range(2)


async def start_handler(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
        ) -> int:
    """Обработчик команды /start"""
    # Инициализируем новую игру
    context.user_data['board'] = Board.create_empty()
    keyboard = generate_keyboard(context.user_data['board'])

    logger.info("User started a new game.")

    await update.message.reply_text(
        'Ваш ход! Поставьте X в свободную клетку',
        reply_markup=keyboard
    )
    return CONTINUE_GAME


async def game_handler(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
        ) -> int:
    """Основной обработчик игры"""
    query = update.callback_query
    await query.answer()  # Отвечаем на callback query

    # Получаем координаты хода игрока
    row, col = map(int, query.data)
    board: Board = context.user_data['board']

    # Проверяем, свободна ли клетка
    if not board.is_cell_free(row, col):
        await query.edit_message_text(
            'Эта клетка уже занята! Выберите другую',
            reply_markup=generate_keyboard(board)
        )
        return CONTINUE_GAME

    # Ход игрока
    board.state[row][col] = Board.CROSS
    logger.info("Player made step.")

    # Проверяем, выиграл ли игрок
    if GameLogic.check_winner(board):
        await query.edit_message_text(
            'Поздравляем! Вы победили! 🎉\nНачните новую игру командой /start',
            reply_markup=generate_keyboard(board)
        )
        logger.info("Player won.")
        return FINISH_GAME

    # Ход бота
    bot_row, bot_col = GameLogic.make_bot_move(board)
    logger.info("Bot made step.")
    if (bot_row, bot_col) == (-1, -1):  # Нет свободных клеток
        await query.edit_message_text(
            'Ничья! 🤝\nНачните новую игру командой /start',
            reply_markup=generate_keyboard(board)
        )
        return FINISH_GAME

    board.state[bot_row][bot_col] = Board.ZERO

    # Проверяем, выиграл ли бот
    if GameLogic.check_winner(board):
        await query.edit_message_text(
            'Бот победил! 🤖\nНачните новую игру командой /start',
            reply_markup=generate_keyboard(board)
        )
        logger.info("Bot won.")
        return FINISH_GAME

    await query.edit_message_text(
        'Ваш ход!',
        reply_markup=generate_keyboard(board)
    )
    return CONTINUE_GAME


async def end_handler(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
        ) -> int:
    """Обработчик завершения игры"""
    query = update.callback_query
    await query.answer()
    context.user_data['board'] = Board.create_empty()
    logger.info("End of game.")
    return ConversationHandler.END
