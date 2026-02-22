import schedule
import time
import sys

import question
import answer
from logger import setup_logger

logger = setup_logger("scheduler")

def run_task(task_func, name):
    logger.info(f"⏳ Executing task: {name}")
    try:
        task_func()
        logger.info(f"✅ Task '{name}' completed successfully.")
    except Exception as e:
        logger.error(f"🚨 Critical failure in '{name}': {e}")

if __name__ == "__main__":
    logger.info("Quiz Bot Scheduler started... 🚀")

    schedule.every().day.at("08:57").do(run_task, question.main, "Daily Question")
    schedule.every().day.at("08:58").do(run_task, answer.main, "Daily Answer")

    while True:
        try:
            schedule.run_pending()
            
            with open("/tmp/heartbeat", "w") as f:
                f.write(str(time.time()))
            
        except Exception as e:
            logger.error(f"Error in scheduler loop: {e}")
        
        time.sleep(1)