import os
import time

import yaml
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

import pubquiztrainer.question as question
import pubquiztrainer.answer as answer
from pubquiztrainer.logger import setup_logger

logger = setup_logger("scheduler")

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CONFIG_PATH = os.path.join(REPO_ROOT, "config.yaml")


def load_schedule_config():
    with open(CONFIG_PATH) as f:
        config = yaml.safe_load(f)
    return config["schedule"]


def run_task(task_func, name):
    logger.info(f"Executing task: {name}")
    try:
        task_func()
        logger.info(f"Task '{name}' completed successfully.")
    except Exception as e:
        logger.error(f"Critical failure in '{name}': {e}")


def heartbeat():
    with open("/tmp/heartbeat", "w") as f:
        f.write(str(time.time()))


def main():
    logger.info("Pub Quiz Bot Scheduler started.")

    schedule_config = load_schedule_config()
    timezone = schedule_config["timezone"]
    question_cron = schedule_config["question"]
    answer_cron = schedule_config["answer"]
    logger.info(f"Timezone: '{timezone}' | Question cron: '{question_cron}' | Answer cron: '{answer_cron}'")

    scheduler = BlockingScheduler(timezone=timezone)
    scheduler.add_job(run_task, CronTrigger.from_crontab(question_cron, timezone=timezone), args=[question.main, "Question"])
    scheduler.add_job(run_task, CronTrigger.from_crontab(answer_cron, timezone=timezone), args=[answer.main, "Answer"])
    scheduler.add_job(heartbeat, "interval", seconds=30)

    scheduler.start()


if __name__ == "__main__":
    main()
