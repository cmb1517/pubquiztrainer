import random

from pubquiztrainer.sources import SOURCES

def get_random_quiz() -> dict:
    source = random.choice(SOURCES)
    return source()

if __name__ == "__main__":
    quiz = get_random_quiz()
    if quiz:
        print(f"Source: {quiz['source']}")
        print(f"Category: {quiz['category']} ({quiz['difficulty']})")
        print(f"Q: {quiz['question']}")
        print(f"Options: {', '.join(quiz['all_options'])}")
        print(f"Correct Answer: {quiz['correct_answer']}")