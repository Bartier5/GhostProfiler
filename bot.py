import logging
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters
)
from config import TELEGRAM_BOT_TOKEN, validate_config
from database import init_db
from handlers import (
    start_handler,
    message_handler,
    profile_handler,
    clear_handler
)
from scheduler import create_scheduler

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)


async def post_init(application):
    await init_db()
    logger.info("database initialized")
    
    scheduler = create_scheduler(application.bot)
    scheduler.start()
    logger.info("scheduler started")


def main():
    validate_config()
    
    app = ApplicationBuilder()\
        .token(TELEGRAM_BOT_TOKEN)\
        .post_init(post_init)\
        .build()
    
    app.add_handler(CommandHandler("start", start_handler))
    app.add_handler(CommandHandler("profile", profile_handler))
    app.add_handler(CommandHandler("clear", clear_handler))
    
    app.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        message_handler
    ))
    
    logger.info("GhostProfiler is running")
    app.run_polling()


if __name__ == "__main__":
    main()