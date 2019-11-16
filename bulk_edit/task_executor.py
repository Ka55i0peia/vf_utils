from bulk_edit.tasks import Task
from typing import List
from collections import deque, abc
from typing import Optional
from dataclasses import dataclass
import datetime
import logging
logger = logging.getLogger(__name__)


class FinishEstimator:

    def __init__(self, allItems: int, windowSize: int = 5):
        self.statisticWindow = windowSize
        self.reset(allItems)

    def reset(self, allItems: int):
        self.allItems = allItems
        self.loopCounter = 0
        # items back in history for average computation
        initialWindow = [None for i in range(self.statisticWindow)]
        self.windowTickTimes = deque(initialWindow, self.statisticWindow)
        self.timePerItem = None

    def percent(self) -> float:
        return 100.0/float(self.allItems) * float(self.loopCounter)

    def items_left(self):
        return self.allItems - self.loopCounter

    def time_until_complete(self) -> str:
        if self.timePerItem is None:
            return "<estimation in progress>"
        else:
            itemsLeft = self.allItems - self.loopCounter
            return f"{int(itemsLeft * self.timePerItem)} sec"

    def tick(self):
        now = datetime.datetime.now()
        self.loopCounter += 1

        firstTimeInWindow = self.windowTickTimes.popleft()

        if firstTimeInWindow:
            windowDelta = now - firstTimeInWindow
            self.timePerItem = float(windowDelta.seconds) / float(self.statisticWindow)

        self.windowTickTimes.append(now)

    def log_progress(self, logger: logging.Logger):
        message = ("Progress: {percent:.2f} % (Left: {no} items in "
                   "approx. {time})").format(percent=self.percent(),
                                             no=self.items_left(),
                                             time=self.time_until_complete())
        logger.info(message)


@dataclass
class ExceptionalTask:
    task: Task
    exception: Exception


class TaskExecutor:

    def __init__(self):
        self.exceptionalTasks: List[ExceptionalTask] = []
        self.executeCount = 0
        self.numberOfTasks = 0

    def _execute_chain(self, tasks: List[Task], input: dict):
        if len(tasks) == 0:
            return

        task = tasks[0]
        if len(tasks) == 1:
            chain = []
        else:
            chain = tasks[1:]

        try:
            # execute task
            output = task.execute(input)

            # output is iterable
            if isinstance(output, abc.Iterable):
                outputItr = iter(output)
                for ithOutput in outputItr:
                    self._execute_chain(chain, ithOutput.payload)

            # task output is not iterable
            else:
                if output.task_succeed:
                    self._execute_chain(chain, output.payload)
                else:
                    logger.error(f"Task '{task.ident()}' execution failed")

        except Exception as ex:
            self.exceptionalTasks.append(ExceptionalTask(task, ex))
            # TODO give the user more info which task fails
            logger.error(f"Exception received while executing a task. Exception: {ex}")
            logger.debug("Trace:\n", exc_info=ex)

    def execute(self, tasks: List[Task]):
        '''
        Executes `tasks`` one by one.
        Between each task a `delay` in seconds can be awaited. (This is useful,
        because VF will block our IP for a curtain time if we fire to much requests
        within a given time period.)
        '''
        self.exceptionalTasks = []

        input = {}
        self._execute_chain(tasks, input)

    def log_summary(self, logger: logging.Logger):

        indent = '\t'
        linebreak = '\n'
        message = []
        fails = len(self.exceptionalTasks)

        if fails > 0:
            message.append("The following tasks failed (executed: {a}, failed: {b}, {p:.2f} "
                           "% fail)".format(a=self.executeCount,
                                            b=fails,
                                            p=100.0/self.executeCount*fails))
        else:
            message.append("All tasks succeeded :)")

        for fail in self.exceptionalTasks:
            message.append(linebreak)
            message.append(indent)
            message.append(fail.task.ident())
            # Get the message from exception. (Selenium pushes an line break at each exception
            # representation). This gets the message or string represantion as fallback:
            exceptionMessage = getattr(fail.exception, 'msg', str(fail.exception))
            message.append(f" (Reason: {exceptionMessage})")

        logger.info(''.join(message))
