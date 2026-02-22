import json
import os

from whatsapp import send_message
from logger import setup_logger

logger = setup_logger("answer")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATE_FILE = os.path.join(BASE_DIR, "today.json")

def main():
    if not os.path.exists(STATE_FILE):
        logger.warning("No active quiz found.")
        return

    with open(STATE_FILE, 'r') as f:
        quiz = json.load(f)

    message = (
        f"💡 *THE REVEAL* 💡\n\n"
        f"The correct answer was:\n"
        f"*({quiz['correct_letter']}) {quiz['correct_answer']}*\n\n"
        f"Did you beat quiz bot today? 🤖"
    )
    send_message(message)
    
    os.remove(STATE_FILE)
    logger.info("Quiz answer sent successfully!")

if __name__ == "__main__":
    main() 