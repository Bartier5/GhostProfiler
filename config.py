import os
from dotenv import load_dotenv
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
DB_PATH="ghostprofiler.db"
TIMEZONE = "Africa/Lagos"

GROQ_MODEL = "llama3-70b-8192"
MIN_MESSAGES_FOR_ANALYSIS = 10

WEEKLY_REPORT_DAY = "sun"
WEEKLY_REPORT_TIME = "08:00"
MONTHLY_REPORT_DAY = 1

ANOMALY_THRESHOLD = 0.15

def validate_config():
    required = {
        "TELEGRAM_BOT_TOKEN": TELEGRAM_BOT_TOKEN,
        "GROQ_API_KEY": GROQ_API_KEY,
    }
    missing = [key for key, val in required.items() if not val]
    if missing:
        raise EnvironmentError(f"Missing env variables: {', '.join(missing)}")