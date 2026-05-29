import aiosqlite
from config import DB_PATH

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""CREATE TABLE IF NOT EXISTS users(
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_active INTEGER DEFAULT 1
        )
                          """)
        await db.execute("""CREATE TABLE IF NOT EXISTS messages(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            content TEXT,
             timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            hour INTEGER,
            day_of_week INTEGER,
            message_length INTEGER,
            sentiment_score REAL DEFAULT NULL,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
                         """)
        await db.execute("""CREATE TABLE IF NOT EXISTS reports(
              id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                report_type TEXT,
                content TEXT,
                generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
                         """)
        await db.commit()
async def register_user(user_id: int, username: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""INSERT OR IGNORE INTO users (user_id, username)
                         VALUES (?, ?)
                         """, (user_id, username))
        await db.commit()
async def save_message(user_id: int, content: str, hour: int, day_of_week: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""INSERT INTO messages (user_id, content, hour, day_of_week, message_length)
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, content, hour, day_of_week, len(content)))
        await db.commit()
async def get_user_messages(user_id: int, days: int = 7):
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("""SELECT content, timestamp, hour, day_of_week, message_length, sentiment_score
            FROM messages
            WHERE user_id = ?
            AND timestamp >= datetime('now', ?)
            ORDER BY timestamp ASC
        """, (user_id, f'-{days} days'))
        rows = await cursor.fetchall()
        return rows
async def update_sentiment(message_id: int, score: float):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            UPDATE messages SET sentiment_score = ? WHERE id = ?
        """, (score, message_id))
        await db.commit()
async def save_report(user_id: int, report_type: str, content: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            INSERT INTO reports (user_id, report_type, content)
            VALUES (?, ?, ?)
        """, (user_id, report_type, content))
        await db.commit()
async def get_message_count(user_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("""
            SELECT COUNT(*) FROM messages WHERE user_id = ?
        """, (user_id,))
        row = await cursor.fetchone()
        return row[0]
async def clear_user_data(user_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("DELETE FROM messages WHERE user_id = ?", (user_id,))
        await db.execute("DELETE FROM reports WHERE user_id = ?", (user_id,))
        await db.commit()