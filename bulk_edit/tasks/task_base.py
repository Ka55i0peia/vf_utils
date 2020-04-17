import abc
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from typing import List


class Task:

    @abc.abstractmethod
    def execute(self) -> bool:
        pass

    def ident(self) -> str:
        return type(self).__name__

    @classmethod
    def parameters(cls) -> List[str]:
        return []


class ComboboxChange(Task):

    def __init__(self, driver: webdriver, changeUrl: str, cmbxHtmlName: str,
                 cmbxTextValue: str):
        self.driver = driver
        self.cmbxTextValue = cmbxTextValue
        # this is the html name property for the custom property drop down (on editfunctions.php)
        self.cmbxHtmlName = cmbxHtmlName
        self.changeUrl = changeUrl

        def ident(self) -> str:
            return (f"Swap combobox value to '{self.cmbxTextValue}' (url={self.changeUrl} "
                    f"comboboxName={self.cmbxHtmlName})")

    @classmethod
    def parameters(cls) -> List[str]:
        return ['changeUrl', 'cmbxHtmlName', 'cmbxTextValue']

    def execute(self) -> bool:
        driver = self.driver

        # open webpage
        driver.get(self.changeUrl)

        # get dropdown element and select value
        combobox = driver.find_element_by_name(self.cmbxHtmlName)
        selector = Select(combobox)
        selector.select_by_visible_text(self.cmbxTextValue)

        # hit the submit method on element. (This lets silenumn walk up the DOM tree
        # to the <form> tag and submit it.)
        combobox.submit()

        # TODO implement a checker for valid input (may make use of JS function: checkMandatory())
        return True


def print_subclass(task_t: type, name_filter: str = '*'):
    for derivedTask in task_t.__subclasses__():
        if name_filter == '*' or name_filter.lower() in derivedTask.__name__.lower():
            # print the task and parameters
            taskName = '{name}\n'
            taskParameter = '  * {parameterName}\n'

            print(taskName.format(name=derivedTask.__name__))
            parameterList = [taskParameter.format(parameterName=p)
                            for p in derivedTask.parameters()]
            print(''.join(parameterList))
        # continue with subclasses (if there are any)
        if len(derivedTask.__subclasses__()) > 0:
            print_subclass(derivedTask, name_filter)