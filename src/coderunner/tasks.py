from celery import shared_task
from celery.utils.log import get_task_logger
from coderunner.runnerfacotry import RunnerNotFound, RunnerFactory
import time
logger = get_task_logger(__name__)

@shared_task
def run_codes(lang_mode, main, sol, testcase):
    logger.info("Get the runner for {lang_mode}".format(lang_mode=lang_mode))
    try:
        factory = RunnerFactory(lang_mode)
    except RunnerNotFound as e:
        message = "An exception of type {0} occurred. Arguments:\n{1!r}"
        return [message.format(type(e).__name__, str(e))]

    runner = factory.create()
    time.sleep(1)
    logger.info("Setup the files for running the codes")
    runner.set_files(main, sol, testcase)
    logger.info("Running the submitted codes")
    return runner.run()