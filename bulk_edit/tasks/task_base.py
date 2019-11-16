import abc
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from typing import Union, Iterable, Optional
import time
from dataclasses import dataclass


class TaskInputMissing(Exception):
    def __init__(self, missingParameter: str):
        super().__init__(f"Input parameter '{missingParameter}' is missing.")
        self.missingParameter = missingParameter


@dataclass
class TaskOutput:
    payload: dict
    task_succeed: bool

    def __setitem__(self, key, item):
        self.payload[key] = item

    def __getitem__(self, key):
        return self.payload[key]


class Task:
    def __init__(self, **static_input):
        self.static_input = static_input

    def execute(self, input: dict) -> Union[TaskOutput, Iterable[TaskOutput]]:
        return TaskOutput(payload=input, task_succeed=True)

    def ident(self) -> str:
        return "Unnamed"

    def get_parameter(self, input: dict, parameter: str, prefer_static: bool = True) -> object:
        if parameter in self.static_input:
            if prefer_static:
                return self.static_input[parameter]
            else:
                if parameter in input:
                    return input[parameter]
                else:
                    return self.static_input[parameter]
        else:
            if parameter in input:
                return input[parameter]
            else:
                raise TaskInputMissing(parameter)


class ComboboxChange(Task):

    def __init__(self, editing_delay: Optional[float] = 1.5, **kwargs):
        # TODO move magic number into config
        super().__init__(self, editing_delay, **kwargs)

    def ident(self) -> str:
        return (f"Swap combobox value")

    def execute(self, input: dict) -> Union[TaskOutput, Iterable[TaskOutput]]:
        output = super().execute(input)

        # TODO think about generating a parameter doc automatic by this calls
        driver = self.get_parameter(input, "webdriver")
        changeUrl = self.get_parameter(input, "url")
        cmbxHtmlName = self.get_parameter(input, "cmbxHtmlName")
        cmbxTextValue = self.get_parameter(input, "cmbxTextValue")
        editing_delay = self.get_parameter(input, "editing_delay")

        # open webpage
        driver.get(changeUrl)

        # get dropdown element and select value
        combobox = driver.find_element_by_name(cmbxHtmlName)
        selector = Select(combobox)
        selector.select_by_visible_text(cmbxTextValue)

        # if a delay is specified, what this time
        # (VF otherwise will block our IP if edits are to often)
        if editing_delay:
            time.sleep(editing_delay)

        # hit the submit method on element. (This lets silenumn walk up the DOM tree
        # to the <form> tag and submit it.)
        combobox.submit()

        # TODO implement a checker for valid input (may make use of JS function: checkMandatory())
        return output
