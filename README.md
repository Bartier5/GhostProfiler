# 👻 GhostProfiler

> *It doesn't reply. It doesn't judge. It just watches.*

GhostProfiler is an experimental, ML-powered Telegram bot that silently absorbs everything you say — rants, vents, 3AM thoughts — and builds a psychological profile of you over time. No commands, no structure, no therapy-speak. Just you talking and the ghost learning.

Every week it tells you what it found. Every month, the full picture.

---

## What Makes It Different

Every journaling or mood-tracking app asks you to **input structured data** — rate your mood 1–10, log your sleep, check a habit. That's conscious and manual.

GhostProfiler does the opposite. It **infers structure from unstructured natural language** passively. You don't know what it's learning. That's the experimental part.

---

## How It Works

```
You send any message (rant, vent, one word, anything)
    → stored silently in PostgreSQL
    → sentiment scored immediately via VADER

Every 6 hours:
    → Isolation Forest runs anomaly detection on your behavior
    → if something's off, you get a quiet alert

Every Sunday 8AM:
    → K-Means clusters your behavioral patterns
    → LDA surfaces recurring themes you didn't notice
    → Ghost Report generated and sent to Telegram

Every 1st of the month:
    → Full Mirror — a complete psychological profile
       built from everything the bot has learned about you
```

---

## Machine Learning Stack

| Algorithm | Purpose |
|---|---|
| **VADER Sentiment** | Scores every message from -1 (dark) to +1 (positive) in real time |
| **K-Means Clustering** | Groups your messages into behavioral modes by time, mood, and length |
| **LDA Topic Modeling** | Finds recurring themes across all your messages without you labeling anything |
| **Isolation Forest** | Learns your behavioral baseline and detects days where something was genuinely off |
| **Association Rule Mining** | Discovers behavioral sequences — e.g. long messages followed by mood drops |

---

## Tech Stack

- **Bot Framework** — `python-telegram-bot` v20 (async)
- **NLP** — `vaderSentiment`, `spaCy`, `nltk`
- **ML** — `scikit-learn`, `gensim`
- **LLM** — Groq API (`llama-3.3-70b-versatile`) for report generation
- **Database** — PostgreSQL via `asyncpg`
- **Scheduler** — `APScheduler`
- **Deployment** — Railway

---

## Project Structure

```
GhostProfiler/
├── main.py            # Entry point
├── config.py          # Environment variables and constants
├── database.py        # PostgreSQL connection and queries
├── handlers.py        # Telegram message and command handlers
├── scheduler.py       # Weekly, monthly, and anomaly jobs
├── preprocessor.py    # Text cleaning, tokenization, entity extraction
├── sentiment.py       # VADER sentiment scoring and trend analysis
├── clustering.py      # K-Means behavioral clustering
├── topics.py          # LDA topic modeling
├── anomaly.py         # Isolation Forest anomaly detection
├── patterns.py        # Time patterns, sequences, vocabulary analysis
├── reporter.py        # ML aggregation and Groq report generation
├── requirements.txt
├── Procfile
└── .gitignore
```

---

## Bot Commands

| Command | What it does |
|---|---|
| `/start` | Register and get the opening message |
| `/profile` | Manually trigger a full profile snapshot |
| `/clear` | Wipe all your data and start fresh |

Everything else you send — every message, rant, thought — is absorbed silently.

---

## Setup & Installation

### Prerequisites
- Python 3.10+
- A Telegram bot token from [@BotFather](https://t.me/BotFather)
- A free Groq API key from [console.groq.com](https://console.groq.com)
- PostgreSQL database (Railway provides one free)

### Local Setup

```bash
# Clone the repo
git clone https://github.com/Bartier5/GhostProfiler.git
cd GhostProfiler

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download spaCy English model
python -m spacy download en_core_web_sm
```

### Environment Variables

Create a `.env` file in the project root:

```env
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
GROQ_API_KEY=your_groq_api_key
DATABASE_URL=your_postgresql_connection_string
```

### Run

```bash
python main.py
```

---

## Deployment (Railway)

1. Push repo to GitHub
2. Create a new project on [Railway](https://railway.app)
3. Deploy from your GitHub repo
4. Add a PostgreSQL database service
5. Set environment variables in the Railway Variables tab
6. Railway auto-deploys on every push

The `Procfile` is already configured:
```
worker: python main.py
```

---

## What the Ghost Reports Look Like

**Weekly Ghost Report** — a cold, data-driven breakdown of your week. No fluff. Direct. Specific.

**Pattern Alert** — fires when anomaly detection catches a behavioral deviation. Doesn't tell you what it is — just that something shifted.

**The Mirror** — monthly. A full psychological profile. Topics you obsess over. Times you're most alive. Patterns you've never consciously noticed. Delivered like a letter from someone who has been watching you silently for 30 days.

---

## Important Notes

- **Minimum 10 messages** required before any analysis runs
- **Groq free tier** has rate limits — space out `/profile` calls
- **PostgreSQL** data persists across redeployments, SQLite does not
- Running the bot locally and on Railway simultaneously with the same token will cause conflicts — only run one instance at a time

---

## Built By

**Anjikwi** — Computer Engineer, Python Developer  
GitHub: [@Bartier5](https://github.com/Bartier5)

---

*GhostProfiler doesn't comfort you. It doesn't encourage you. It just holds up a mirror.*
