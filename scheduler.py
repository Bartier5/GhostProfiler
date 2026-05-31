import pytz
import logging
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from config import (
    TIMEZONE,
    WEEKLY_REPORT_DAY,
    WEEKLY_REPORT_TIME,
    MONTHLY_REPORT_DAY,
    MIN_MESSAGES_FOR_ANALYSIS
)
from database import get_user_messages, save_report
from reporter import generate_and_save_report
from anomaly import detect_anomalies

logger = logging.getLogger(__name__)
tz = pytz.timezone(TIMEZONE)


async def send_weekly_reports(bot):
    logger.info("weekly report job started")
    
    from database import DB_PATH
    import aiosqlite
    
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "SELECT user_id FROM users WHERE is_active = 1"
        )
        users = await cursor.fetchall()
    
    for (user_id,) in users:
        try:
            messages = await get_user_messages(user_id, days=7)
            
            if len(messages) < MIN_MESSAGES_FOR_ANALYSIS:
                continue
            
            report = await generate_and_save_report(
                user_id=user_id,
                messages=messages,
                report_type="weekly",
                save_func=save_report
            )
            
            await bot.send_message(
                chat_id=user_id,
                text=f"👻 weekly ghost report\n\n{report}"
            )
            
        except Exception as e:
            logger.error(f"weekly report failed for {user_id}: {e}")


async def send_monthly_reports(bot):
    logger.info("monthly mirror job started")
    
    from database import DB_PATH
    import aiosqlite
    
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "SELECT user_id FROM users WHERE is_active = 1"
        )
        users = await cursor.fetchall()
    
    for (user_id,) in users:
        try:
            messages = await get_user_messages(user_id, days=30)
            
            if len(messages) < MIN_MESSAGES_FOR_ANALYSIS:
                continue
            
            report = await generate_and_save_report(
                user_id=user_id,
                messages=messages,
                report_type="monthly",
                save_func=save_report
            )
            
            await bot.send_message(
                chat_id=user_id,
                text=f"🪞 the mirror\n\n{report}"
            )
            
        except Exception as e:
            logger.error(f"monthly report failed for {user_id}: {e}")


async def check_anomalies(bot):
    logger.info("anomaly check started")
    
    from database import DB_PATH
    import aiosqlite
    
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "SELECT user_id FROM users WHERE is_active = 1"
        )
        users = await cursor.fetchall()
    
    for (user_id,) in users:
        try:
            messages = await get_user_messages(user_id, days=14)
            
            if len(messages) < MIN_MESSAGES_FOR_ANALYSIS:
                continue
            
            result = detect_anomalies(messages)
            
            if result['anomaly_count'] > 0:
                await bot.send_message(
                    chat_id=user_id,
                    text=(
                        "👁️ pattern detected.\n\n"
                        "something in your behavior shifted recently.\n"
                        "run /profile to see the full picture."
                    )
                )
        except Exception as e:
            logger.error(f"anomaly check failed for {user_id}: {e}")


def create_scheduler(bot) -> AsyncIOScheduler:
    scheduler = AsyncIOScheduler(timezone=tz)
    
    scheduler.add_job(
        send_weekly_reports,
        trigger=CronTrigger(
            day_of_week=WEEKLY_REPORT_DAY,
            hour=int(WEEKLY_REPORT_TIME.split(":")[0]),
            minute=int(WEEKLY_REPORT_TIME.split(":")[1]),
            timezone=tz
        ),
        args=[bot],
        id="weekly_reports",
        replace_existing=True
    )
    
    scheduler.add_job(
        send_monthly_reports,
        trigger=CronTrigger(
            day=MONTHLY_REPORT_DAY,
            hour=8,
            minute=0,
            timezone=tz
        ),
        args=[bot],
        id="monthly_reports",
        replace_existing=True
    )
    
    scheduler.add_job(
        check_anomalies,
        trigger=CronTrigger(
            hour="*/6",
            timezone=tz
        ),
        args=[bot],
        id="anomaly_check",
        replace_existing=True
    )
    
    return scheduler