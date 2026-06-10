# Pub Quiz Trainer Bot

A WhatsApp bot that sends your group a trivia question every two hours and reveals the answer 30 minutes later — keeping your pub quiz team sharp between sessions.

Questions are sourced from the [Open Trivia DB](https://opentdb.com/) and delivered via [WAHA](https://waha.devlike.pro/) (self-hosted WhatsApp HTTP API).

---

## Table of contents

- [How it works](#how-it-works)
- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [Running](#running)
- [Project structure](#project-structure)

---

## How it works

The scheduler fires two jobs on a repeating cycle:

| Time | Job |
|------|-----|
| `:00` every 2 hours | Fetches a weighted-random question and sends it to the group |
| `:30` every 2 hours | Reveals the correct answer |

Category selection is weighted — General Knowledge, Geography, and History appear more often than niche categories like Anime or Video Games. Weights are configurable in `src/pubquiztrainer/quiz.py`.

---

## Prerequisites

- Python 3.13+
- [`uv`](https://github.com/astral-sh/uv) (package manager)
- A running WAHA instance (see [WAHA docs](https://waha.devlike.pro/))
- A WhatsApp group chat ID

---

## Setup

**1. Clone and install dependencies**

```bash
git clone https://github.com/your-username/pubquiztrainer.git
cd pubquiztrainer
uv sync
```

**2. Configure environment variables**

Copy `.env` and fill in your values:

```bash
cp .env .env.local
```

| Variable | Description |
|---|---|
| `WAHA_URL` | Base URL of your WAHA instance (e.g. `http://localhost:3000`) |
| `WAHA_API_KEY` | API key configured in WAHA |
| `WHATSAPP_GROUP_ID` | Target WhatsApp group ID (e.g. `123456789@g.us`) |

---

## Running

**Locally**

```bash
# Start the scheduler (runs continuously)
uv run -m pubquiztrainer.scheduler

# Fire jobs manually for testing
uv run -m pubquiztrainer.question   # send a question now
uv run -m pubquiztrainer.answer     # reveal the answer now
```

**Docker Compose (recommended for production)**

```bash
docker compose up --build
```

This starts both the WAHA engine and the quiz bot. WAHA's dashboard is available at `http://localhost:3000` — use it to scan the WhatsApp QR code on first run.

**Docker only**

```bash
docker build -t pubquiztrainer .
docker run --env-file .env pubquiztrainer
```

---

## Project structure

```
src/pubquiztrainer/
├── scheduler.py    # Entry point — schedules question and answer jobs
├── quiz.py         # Fetches questions from Open Trivia DB (weighted categories)
├── question.py     # Formats and sends the question; persists state to today.json
├── answer.py       # Reads state, sends the reveal, cleans up today.json
├── whatsapp.py     # WAHA API client with session health checks
├── decorators.py   # @retry decorator (exponential backoff + jitter)
└── logger.py       # Stdout logger setup
```
