from typing import TypedDict

from pubquiztrainer.sources import opentrivia, thetriviaapi

class QuizQuestion(TypedDict):
    question: str
    correct_answer: str
    all_options: list[str]
    category: str
    difficulty: str
    source: str


SOURCES = [
    opentrivia.get_random_quiz,
    thetriviaapi.get_random_quiz,
]