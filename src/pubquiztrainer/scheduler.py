import schedule
import time
import sys

import pubquiztrainer.question as question
import pubquiztrainer.answer as answer
from pubquiztrainer.logger import setup_logger

logger = setup_logger("scheduler")


def run_task(task_func, name):
    logger.info(f"Executing task: {name}")
    try:
        task_func()
        logger.info(f"Task '{name}' completed successfully.")
    except Exception as e:
        logger.error(f"Critical failure in '{name}': {e}")


QUESTION_TIMES = ["09:00", "11:00", "13:00", "15:00", "17:00", "19:00", "21:00"]
ANSWER_TIMES = ["09:30", "11:30", "13:30", "15:30", "17:30", "19:30", "21:30"]


def main():
    logger.info("Pub Quiz Bot Scheduler started.")
    logger.info("Mode: Question every 2 hours from 09:00 to 21:00 (Answer 30 mins later)")

    for t in QUESTION_TIMES:
        schedule.every().day.at(t).do(run_task, question.main, "Question")
    for t in ANSWER_TIMES:
        schedule.every().day.at(t).do(run_task, answer.main, "Answer")

    while True:
        try:
            schedule.run_pending()

            with open("/tmp/heartbeat", "w") as f:
                f.write(str(time.time()))

        except Exception as e:
            logger.error(f"Error in scheduler loop: {e}")

        time.sleep(1)


if __name__ == "__main__":
    main()