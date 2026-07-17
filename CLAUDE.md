# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install dependencies
uv sync

# Run the scheduler (main entry point)
uv run -m pubquiztrainer.scheduler

# Run jobs manually (useful for testing)
uv run -m pubquiztrainer.question   # fetch question and send to WhatsApp
uv run -m pubquiztrainer.answer     # reveal answer and clear state

# Inspect quiz fetching in isolation
uv run -m pubquiztrainer.quiz       # prints a sample question to stdout

# Docker
docker compose up --build
```

There is no test suite currently.

## Architecture

The bot sends a trivia question to a WhatsApp group, then reveals the answer 30 minutes later, on a schedule defined by cron expressions in `config.yaml` (repo root).

**Flow:**

```
config.yaml   →  schedule.question (cron) ┐
                  schedule.answer (cron)   │
scheduler.py  →  APScheduler CronTrigger jobs → question.main()
                                            └→ answer.main()
```

1. `question.main()` calls `quiz.get_random_quiz()` (Open Trivia DB API), persists the result to `today.json` (stored inside the package directory next to the source files), then sends the formatted question via `whatsapp.send_message()`.
2. `answer.main()` reads `today.json`, sends the reveal message, then deletes the file. If the file is missing, it no-ops.

**Key design points:**

- **Schedule config** — `scheduler.py` loads `config.yaml` at startup and registers `schedule.question` / `schedule.answer` (standard 5-field cron expressions) as APScheduler `CronTrigger` jobs, evaluated in `schedule.timezone` (an IANA name, e.g. `Europe/London`) so times stay correct across DST changes regardless of the container's system timezone. Change the timing by editing `config.yaml`; no code changes needed.
- **Category weighting** — `quiz.py` defines `CATEGORY_WEIGHTS` (a dict of Open Trivia DB category IDs → relative weights). `random.choices` picks a category each call. Adjust weights there to bias question topics.
- **Retry decorator** — `decorators.retry` (exponential backoff + jitter) wraps both `get_random_quiz` and `send_message`. Category-exhausted responses from the API (`response_code` 1 or 4) are treated as retryable exceptions.
- **WAHA client** — `whatsapp.py` talks to [WAHA](https://waha.devlike.pro/) (self-hosted WhatsApp HTTP API). `WAHA_URL` is parsed by stripping `/api` and trailing slashes, so either a base URL or a full endpoint URL works. `ensure_session_working()` checks the session status before every send and attempts to restart it if needed, letting the retry decorator handle the actual retry.
- **Health check** — the scheduler writes `time.time()` to `/tmp/heartbeat` every 30 seconds; Docker Compose checks this file is newer than 2 minutes.

## Environment Variables

Set in `.env` (loaded by Docker Compose):

| Variable | Description |
|---|---|
| `WAHA_URL` | Base URL for WAHA (default: `http://waha:3000`) |
| `WAHA_API_KEY` | API key for WAHA authentication |
| `WHATSAPP_GROUP_ID` | WhatsApp group chat ID (e.g. `123456@g.us`) |

In Docker Compose, the `quiz-bot` container connects to the `waha` service by hostname. Locally, `WAHA_URL` defaults to `http://localhost:3000` so a locally-running WAHA instance works without any extra config.
