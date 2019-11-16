from bulk_edit import log, TaskExecutor, tasks
import logging
logger = logging.getLogger(__name__)


class StringLogger:
    def __init__(self, *args, **kwargs):
        self.messages = []

    def info(self, message: str):
        self.messages.append(message)
        logger.info(f"StringLogger: {message}")


def test_task_execution():
    schedule = []

    schedule.append(tasks.dummies.DataSource())
    schedule.append(tasks.dummies.Appender(name="A"))
    schedule.append(tasks.dummies.Splitter())
    schedule.append(tasks.dummies.Appender(name="B"))
    schedule.append(tasks.dummies.Appender(name="C"))
    outputChecker = StringLogger()
    schedule.append(tasks.dummies.Printer(logger=outputChecker))
    executor = TaskExecutor()
    executor.execute(schedule)
    assert len( outputChecker.messages ) == 2
    assert outputChecker.messages[0] == ':Start:->A->Path1:->B->C'
    assert outputChecker.messages[1] == ':Start:->A->Path2:->B->C'


if __name__ == "__main__":
    log.load_config()
    test_task_execution()
