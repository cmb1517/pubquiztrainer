import random

from pubquiztrainer.sources import SOURCES
from pubquiztrainer.logger import setup_logger

logger = setup_logger("quiz")

def get_random_quiz() -> dict:
    source = random.choice(SOURCES)
    logger.info(f"Selected trivia source: {source.__module__}")
    return source()

if __name__ == "__main__":
    quiz = get_random_quiz()
    if quiz:
        print(f"Source: {quiz['source']}")
        print(f"Category: {quiz['category']} ({quiz['difficulty']})")
        print(f"Q: {quiz['question']}")
        print(f"Options: {', '.join(quiz['all_options'])}")
        print(f"Correct Answer: {quiz['correct_answer']}")