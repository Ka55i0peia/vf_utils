import abc
from selenium import webdriver
from selenium.webdriver.support.ui import Select


class Task:

    @abc.abstractmethod
    def execute(self) -> bool:
        pass

    def ident(self) -> str:
        return "Unnamed"


class ComboboxChange(Task):

    def __init__(self, webdriver: webdriver, changeUrl: str, cmbxHtmlName: str,
                 cmbxTextValue: str):
        self.webdriver = webdriver
        self.cmbxTextValue = cmbxTextValue
        # this is the html name property for the custom property drop down (on editfunctions.php)
        self.cmbxHtmlName = cmbxHtmlName
        self.changeUrl = changeUrl

        def ident(self) -> str:
            return (f"Swap combobox value to '{self.cmbxTextValue}' (url={self.changeUrl} "
                    f"comboboxName={self.cmbxHtmlName})")

    def execute(self) -> bool:
        driver = self.webdriver

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
