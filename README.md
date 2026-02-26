A mildly over-engineered, mission-critical Pub Quiz Training Bot that fetches questions from the Open Trivia DB API, pipes them through a Python backend, and deploys them via a WAHA-powered WhatsApp integration—because nothing says “we’re here to win” like distributed trivia delivery infrastructure and an unhealthy commitment to pub supremacy. 🍻

### How to run

- **Prerequisites**
  - **Python**: 3.13+
  - **Dependencies**: managed via `uv` and `pyproject.toml`

- **Install dependencies (dev)**

```bash
uv sync
```

- **Run the scheduler locally**

```bash
uv run -m pubquiztrainer.scheduler
```

- **Run individual jobs manually**

```bash
uv run -m pubquiztrainer.question
uv run -m pubquiztrainer.answer
```

- **Run via Docker / Docker Compose**
  - **Docker**: the image’s default command runs the scheduler:

    ```bash
    docker build -t pubquiztrainer .
    docker run --env-file .env pubquiztrainer
    ```

  - **Docker Compose**:

    ```bash
    docker compose up --build
    ```