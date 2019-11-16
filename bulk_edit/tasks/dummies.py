from .task_base import Task, TaskOutput
from typing import Union, Iterable
import logging
logger = logging.getLogger(__name__)


class DataSource(Task):
    def execute(self, input: dict) -> Union[TaskOutput, Iterable[TaskOutput]]:
        output = super().execute(input)
        output["data"] = ':Start:'
        return output


class Appender(Task):
    def ident(self) -> str:
        return f"Appender"

    def execute(self, input: dict) -> Union[TaskOutput, Iterable[TaskOutput]]:
        output = super().execute(input)

        name = self.get_parameter(input, "name")
        data = self.get_parameter(input, "data")
        output["data"] = data + "->" + name
        return output


class Splitter(Task):
    def ident(self) -> str:
        return f"Appender"

    def execute(self, input: dict) -> Union[TaskOutput, Iterable[TaskOutput]]:
        output = super().execute(input)

        data = self.get_parameter(input, "data")
        output["data"] = data + "->Path1:"
        yield output
        output["data"] = data + "->Path2:"
        yield output


class Printer(Task):
    def __init__(self, logger, **static_input):
        self.logger = logger
        super().__init__(**static_input)

    def ident(self) -> str:
        return f"Printer"

    def execute(self, input: dict) -> Union[TaskOutput, Iterable[TaskOutput]]:
        output = super().execute(input)

        data = self.get_parameter(input, "data")
        self.logger.info(data)

        return output
