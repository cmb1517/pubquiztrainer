import requests
import html
import random

from decorators import retry

@retry(max_tries=5, initial_delay=1, backoff_factor=2)
def get_random_quiz():
    """
    Fetches 1 random multiple choice question from Open Trivia DB.
    Returns a dictionary or None if the request fails.
    """
    # API Params: 1 question, multiple choice (default is any category/difficulty)
    URL = "https://opentdb.com/api.php?amount=1&type=multiple"
    # URL = "https://opentdb.com/api.php?amount=1&category=9&difficulty=hard&type=multiple"
    
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
        else:
            print(f"API Error: Response code {data.get('response_code')}")
            return None

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