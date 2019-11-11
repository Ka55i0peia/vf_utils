from typing import List
from tasks import Task
import datetime
import logging
logger = logging.getLogger(__name__)


class FinishEstimator:

    def __init__(self, allItems: int):
        self.reset(allItems)

    def reset(self, allItems: int):
        self.allItems = allItems
        self.loopCounter = 0
        # items back in history for average computation
        self.statisticWindow = 5
        self.timeOfWindowBegin = None
        self.timeOnLastTick = None
        self.timePerItem = None

    def percent(self) -> float:
        return 100.0/float(self.allItems) * float(self.loopCounter)

    def timeUntilComplete(self) -> str:
        if self.timePerItem is None:
            return "estimation in progress"
        else:
            itemsLeft = self.allItems - self.loopCounter
            return f"{itemsLeft * self.timePerItem} sec"

    def tick(self):
        self.loopCounter += 1

        if self.timeOfWindowBegin is None:
            self.timeOfWindowBegin = datetime.datetime.now()

        # time measurements inside moving window
        if self.loopCounter > self.statisticWindow - 1:
            now = datetime.datetime.now()
            tickDelta = now - self.timeOnLastTick
            windowDelta = now - self.timeOfWindowBegin

            self.timePerItem = float(windowDelta.seconds) / float(self.statisticWindow)
            self.timeOfWindowBegin = self.timeOfWindowBegin + tickDelta

        self.timeOnLastTick = datetime.datetime.now()


class TaskExecutor:

    def __init__(self):
        self.exceptionalTasks: List[Task] = []

    def execute(self, tasks: List[Task]):
        numberOfTasks = len(tasks)
        progress = FinishEstimator(numberOfTasks)

        for task in tasks:
            try:
                task.execute()

            except Exception as ex:
                self.exceptionalTasks.append(task)
                # TODO give the user more info which task fails
                logger.error(f"Exception received while executing a task. Exception: {ex}")
                logger.debug("Trace:\n", exc_info=ex)

            # some statistics
            progress.tick()
            logger.info(f"Progress: {progress.percent()} % (Time left: {progress.timeUntilComplete()})")
