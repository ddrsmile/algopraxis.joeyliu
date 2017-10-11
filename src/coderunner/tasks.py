# -*- coding: utf-8 -*-
from celery import shared_task
from celery.utils.log import get_task_logger
from coderunner.runnerfacotry import RunnerNotFound, RunnerFactory
logger = get_task_logger(__name__)

@shared_task(max_retries=3,soft_time_limit=5)
def run_codes(lang_mode, main, sol, testcase):
    try:
        factory = RunnerFactory(lang_mode)
        runner = factory.create()
        results = runner.run(main, sol, testcase)
        return results
    except RunnerNotFound:
        return ["The runner for language mode, {}, was not found!".format(lang_mode)]
    except Exception as e:
        message = "An exception of type {0} occurred in run_codes method. \n{1}"
        return [message.format(type(e).__name__, str(e))]