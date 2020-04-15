from bulk_edit import tasks, log, TaskExecutor
from bulk_edit.tasks.members import community as community_task
import atexit
import logging
logger = logging.getLogger(__name__)


if __name__ == '__main__':
    log.load_config()
    try:
        login = tasks.LoginToVf(headlessMode=False)

        login.execute()
        driver = login.webdriver

        # prepare task list
        # TODO provide a CLI!
        #      params: 
        #         * task name
        #         * task data as key value list
        #      TODO let the Task returns it's parameter
        #         * support cli by returning possible keys for a given task name
        taskList = []
        with open("input/mustermann.txt", "r") as f:
            line = f.readline()
            while line:
                # prepare task
                taskParameter = {
                    "webdriver": driver,
                    "uid": int(line),
                    "costType": "Zukunftsfond",
                    "comment": "test",
                    "validFrom": "1.1.2020",
                    "validTo": "31.12.2020"
                }
                task = community_task.AddCommunityCosts
                taskList.append(task(**taskParameter))
                # makes this loop a for each line
                line = f.readline()

        batchProcess = TaskExecutor()
        # log process results in every state (even it's interrupted by user or exception)
        atexit.register(batchProcess.log_summary, logger)
        # executes all tasks
        batchProcess.execute(taskList)

    except KeyboardInterrupt:
        logger.info("User interrupted")

    except Exception as ex:
        logger.error(ex)
        logger.debug("Trace:\n", exc_info=ex)
