import json
import os

from pubquiztrainer.whatsapp import send_message
from pubquiztrainer.logger import setup_logger

logger = setup_logger("answer")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATE_FILE = os.path.join(BASE_DIR, "today.json")

def main():
    if not os.path.exists(STATE_FILE):
        logger.warning(f"No active quiz found at {STATE_FILE}; skipping answer reveal.")
        return

    logger.info(f"Reading quiz state from {STATE_FILE}")
    with open(STATE_FILE, 'r') as f:
        quiz = json.load(f)
    logger.info("Quiz state loaded successfully.")

    message = (
        f"💡 *THE REVEAL* 💡\n\n"
        f"The correct answer was:\n"
        f"*({quiz['correct_letter']}) {quiz['correct_answer']}*\n\n"
        f"Did you beat quiz bot today? 🤖"
    )
    send_message(message)
    logger.info("Quiz answer sent successfully.")

    os.remove(STATE_FILE)
    logger.info(f"Quiz state file {STATE_FILE} removed.")

if __name__ == "__main__":
    main() 