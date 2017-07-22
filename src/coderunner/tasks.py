from celery import shared_task
from celery.utils.log import get_task_logger
from coderunner.src.runner import run
import time
logger = get_task_logger(__name__)

@shared_task
def run_codes(main_content, sol_content, input_data):
    logger.info("Wait for at least 1s")
    time.sleep(1)
    logger.info("Run submitted codes")
    return run(main_content, sol_content, input_data)