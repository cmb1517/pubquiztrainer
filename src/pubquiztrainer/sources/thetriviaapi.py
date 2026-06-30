import requests
import random

from pubquiztrainer.decorators import retry
from pubquiztrainer.logger import setup_logger

logger = setup_logger("sources.thetriviaapi")

CATEGORY_WEIGHTS = {
    "general_knowledge": 20,
    "history": 10,
    "geography": 8,
    "film_and_tv": 8,
    "science": 10,
    "arts_and_literature": 6,
    "sports_and_leisure": 6,
    "music": 5,
    "food_and_drink": 4,
    "society_and_culture": 3,
}

def get_weighted_category():
    categories = list(CATEGORY_WEIGHTS.keys())
    weights = list(CATEGORY_WEIGHTS.values())
    return random.choices(categories, weights=weights, k=1)[0]

@retry(max_tries=5, initial_delay=1, backoff_factor=2)
def get_random_quiz() -> dict:
    selected_category = get_weighted_category()
    logger.info(f"Fetching question from The Trivia API (category: {selected_category})")
    url = f"https://the-trivia-api.com/v2/questions?limit=1&categories={selected_category}&types=text_choice"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if not data:
            raise Exception(f"No results for category '{selected_category}'")
        
        result = data[0]
        correct_answer = result["correctAnswer"]
        incorrect_answers = result["incorrectAnswers"]

        options = incorrect_answers + [correct_answer]
        random.shuffle(options)

        return {
            "question": result["question"]["text"],
            "correct_answer": correct_answer,
            "all_options": options,
            "category": result["category"].replace("_", " ").title(),
            "difficulty": result["difficulty"].capitalize(),
            "source": "The Trivia API",
        }
    
    except Exception as e:
        logger.error(f"Error fetching trivia: {e}")
        raise

if __name__ == "__main__":
    quiz = get_random_quiz()
    if quiz:
        print(f"Category: {quiz['category']} ({quiz['difficulty']})")
        print(f"Q: {quiz['question']}")
        print(f"A: {quiz['correct_answer']}")
        print(f"Options: {', '.join(quiz['all_options'])}")