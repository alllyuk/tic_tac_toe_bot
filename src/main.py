import os
from dotenv import load_dotenv

from telegram import Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
)

from .bot.handlers import (
    start_handler,
    game_handler,
    end_handler,
    CONTINUE_GAME,
    FINISH_GAME
)

from src.logger import logger

# Загружаем переменные окружения
load_dotenv()


def create_application() -> Application:
    """Создание и настройка приложения"""
    token = os.getenv('TG_TOKEN')
    if not token:
        raise ValueError("Не задан токен бота в переменных окружения")

    return Application.builder().token(token).build()


def setup_handlers(application: Application) -> None:
    """Настройка обработчиков команд"""
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start_handler)],
        states={
            CONTINUE_GAME: [
                CallbackQueryHandler(game_handler, pattern=f'^{r}{c}$')
                for r in range(3)
                for c in range(3)
            ],
            FINISH_GAME: [
                CallbackQueryHandler(end_handler, pattern=f'^{r}{c}$')
                for r in range(3)
                for c in range(3)
            ],
        },
        fallbacks=[CommandHandler('start', start_handler)],
    )

    application.add_handler(conv_handler)


def main() -> None:
    """Основная функция запуска бота"""
    try:
        # Создаем и настраиваем приложение
        application = create_application()
        setup_handlers(application)

        # Запускаем бота
        logger.info("Бот запущен")
        application.run_polling(allowed_updates=Update.ALL_TYPES)

    except Exception as e:
        logger.error(f"Ошибка при запуске бота: {e}")
        raise


if __name__ == '__main__':
    main()
