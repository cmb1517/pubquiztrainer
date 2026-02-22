import json
import os

from quiz import get_random_quiz
from whatsapp import send_message
from logger import setup_logger

logger = setup_logger("question")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATE_FILE = os.path.join(BASE_DIR, "today.json")

def main():
    logger.info("Starting daily quiz generation...")
    quiz = get_random_quiz()
    if not quiz:
        logger.warning("Could not fetch quiz today.")
        return

    letters = ["A", "B", "C", "D"]
    formatted_options = []
    
    correct_letter = ""
    
    for i, option in enumerate(quiz['all_options']):
        letter = letters[i]
        if option == quiz['correct_answer']:
            correct_letter = letter
        formatted_options.append(f"*{letter})* {option}")

    quiz['correct_letter'] = correct_letter
    quiz['formatted_options_text'] = "\n".join(formatted_options)

    with open(STATE_FILE, 'w') as f:
        json.dump(quiz, f)

    message = (
        f"☀️ *DAILY PUB QUIZ* ☀️\n\n"
        f"*Category:* {quiz['category']}\n"
        f"*Difficulty:* {quiz['difficulty']}\n\n"
        f"*{quiz['question']}*\n\n"
        f"{quiz['formatted_options_text']}\n\n"
        f"--- \n"
        f"Reply with your guess! The answer will be revealed in 1 hour. 🕒"
    )

    send_message(message)
    logger.info("Quiz question sent successfully!")

if __name__ == "__main__":
    main()