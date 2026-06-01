import asyncpg
import os
from config import DB_PATH

DATABASE_URL = os.getenv("DATABASE_URL")


async def get_connection():
    return await asyncpg.connect(DATABASE_URL)


async def init_db():
    conn = await get_connection()
    try:
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id BIGINT PRIMARY KEY,
                username TEXT,
                joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_active INTEGER DEFAULT 1
            )
        """)
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id SERIAL PRIMARY KEY,
                user_id BIGINT,
                content TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                hour INTEGER,
                day_of_week INTEGER,
                message_length INTEGER,
                sentiment_score REAL DEFAULT NULL,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS reports (
                id SERIAL PRIMARY KEY,
                user_id BIGINT,
                report_type TEXT,
                content TEXT,
                generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)
    finally:
        await conn.close()


async def register_user(user_id: int, username: str):
    conn = await get_connection()
    try:
        await conn.execute("""
            INSERT INTO users (user_id, username)
            VALUES ($1, $2)
            ON CONFLICT (user_id) DO NOTHING
        """, user_id, username)
    finally:
        await conn.close()


async def save_message(user_id: int, content: str, hour: int, day_of_week: int):
    conn = await get_connection()
    try:
        await conn.execute("""
            INSERT INTO messages (user_id, content, hour, day_of_week, message_length)
            VALUES ($1, $2, $3, $4, $5)
        """, user_id, content, hour, day_of_week, len(content))
    finally:
        await conn.close()


async def get_user_messages(user_id: int, days: int = 7):
    conn = await get_connection()
    try:
        rows = await conn.fetch(f"""
            SELECT content, timestamp::text, hour, day_of_week,
            message_length, sentiment_score
            FROM messages
            WHERE user_id = $1
            AND timestamp >= NOW() - INTERVAL '{days} days'
            ORDER BY timestamp ASC
        """, user_id)
        return [tuple(row) for row in rows]
    finally:
        await conn.close()


async def update_sentiment(message_id: int, score: float):
    conn = await get_connection()
    try:
        await conn.execute("""
            UPDATE messages SET sentiment_score = $1 WHERE id = $2
        """, score, message_id)
    finally:
        await conn.close()


async def save_report(user_id: int, report_type: str, content: str):
    conn = await get_connection()
    try:
        await conn.execute("""
            INSERT INTO reports (user_id, report_type, content)
            VALUES ($1, $2, $3)
        """, user_id, report_type, content)
    finally:
        await conn.close()


async def get_message_count(user_id: int):
    conn = await get_connection()
    try:
        result = await conn.fetchval("""
            SELECT COUNT(*) FROM messages WHERE user_id = $1
        """, user_id)
        return result
    finally:
        await conn.close()


async def clear_user_data(user_id: int):
    conn = await get_connection()
    try:
        await conn.execute(
            "DELETE FROM messages WHERE user_id = $1", user_id
        )
        await conn.execute(
            "DELETE FROM reports WHERE user_id = $1", user_id
        )
    finally:
        await conn.close()