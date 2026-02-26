import requests
import html
import random

from pubquiztrainer.decorators import retry

CATEGORY_WEIGHTS = {
    9: 20,  # General Knowledge (20% chance)
    10: 5,  # Books
    11: 5,  # Film
    12: 5,  # Music
    13: 2,  # Musicals
    14: 5,  # TV
    15: 1,  # Video Games (Very Rare)
    16: 2,  # Board Games
    17: 8,  # Science & Nature
    18: 3,  # Computers
    19: 2,  # Math
    20: 3,  # Mythology
    21: 5,  # Sports
    22: 10, # Geography
    23: 10, # History
    24: 2,  # Politics
    25: 3,  # Art
    26: 2,  # Celebrities
    27: 3,  # Animals
    28: 2,  # Vehicles
    29: 1,  # Comics
    30: 2,  # Gadgets
    31: 1,  # Anime
    32: 1   # Cartoons
}

def get_weighted_category():
    """Selects a category ID based on the defined weights."""

    categories = list(CATEGORY_WEIGHTS.keys())
    weights = list(CATEGORY_WEIGHTS.values())

    return random.choices(categories, weights=weights, k=1)[0]

@retry(max_tries=5, initial_delay=1, backoff_factor=2)
def get_random_quiz():
    """
    Fetches 1 random multiple choice question from Open Trivia DB.
    Returns a dictionary or None if the request fails.
    """
    # API Params: 1 question, multiple choice (default is any category/difficulty)
    # URL = "https://opentdb.com/api.php?amount=1&type=multiple"
    # URL = "https://opentdb.com/api.php?amount=1&category=9&difficulty=hard&type=multiple"

    selected_category_id = get_weighted_category()

    URL = f"https://opentdb.com/api.php?amount=1&category={selected_category_id}&type=multiple"
    
    try:
        response = requests.get(URL, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data.get("response_code") == 0:
            result = data["results"][0]
            
            question = html.unescape(result["question"])
            correct_answer = html.unescape(result["correct_answer"])
            incorrect_answers = [html.unescape(ans) for ans in result["incorrect_answers"]]
            
            options = incorrect_answers + [correct_answer]
            random.shuffle(options)

            return {
                "question": question,
                "correct_answer": correct_answer,
                "all_options": options,
                "category": result["category"],
                "difficulty": result["difficulty"].capitalize()
            }
        
        elif data.get("response_code") in [1, 4]:
            print(f"Category {selected_category_id} exhausted or no results. Retrying...")
            raise Exception("Category Exhausted")

    except Exception as e:
        print(f"Error fetching trivia: {e}")
        return None

if __name__ == "__main__":
    quiz = get_random_quiz()
    if quiz:
        print(f"Category: {quiz['category']} ({quiz['difficulty']})")
        print(f"Q: {quiz['question']}")
        print(f"Options: {', '.join(quiz['all_options'])}")
        print(f"A: {quiz['correct_answer']}")