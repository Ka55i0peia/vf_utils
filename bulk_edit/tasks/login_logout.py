from bulk_edit.tasks import Task, TaskOutput
from typing import Union, Iterable
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException


class CreateFirefoxControl(Task):
    def __init__(self, headlessMode: bool):
        self.headlessMode = False

    def ident(self) -> str:
        return f"Create firefox control"

    def execute(self, input: dict) -> Union[TaskOutput, Iterable[TaskOutput]]:
        output = super().execute(input)

        profile = webdriver.FirefoxProfile()
        options = Options()
        # this line starts FF in headless mode
        options.headless = self.headlessMode
        driver = webdriver.Firefox(firefox_profile=profile, options=options)

        output["webdriver"] = driver
        return output


class LoginToVf(Task):

    def __init__(self, credentialFile: str = "vf_login_credentials.txt"):
        self.credentialFile = credentialFile

    def ident(self) -> str:
        return f"VF Login with credentialFile '{self.credentialFile}'"

    # NOTE candidate for global utility
    @staticmethod
    def get_user_and_passwd_from_file(fileName: str) -> (str, str):
        user = None
        pwd = None
        with open(fileName, 'r') as f:
            # first line:
            user = f.readline()
            # second line:
            pwd = f.readline()

        # error check
        if len(user) == 0 or len(pwd) == 0:
            raise Exception(f"Crendential file '{fileName}' must contain a user "
                            "in the first line and password in the second line")

        return (user, pwd)

    def execute(self, input: dict) -> Union[TaskOutput, Iterable[TaskOutput]]:
        output = super().execute(input)

        driver = Task.get_parameter(input, "webdriver")
        driver.get("https://vereinsflieger.de/")

        # check if we are already logged in ..
        try:
            driver.find_element_by_link_text("Mein Profil")
            return output
        except NoSuchElementException:
            # no, we aren't logged in already
            pass

        # login
        (user, pwd) = type(self).get_user_and_passwd_from_file(self.credentialFile)
        driver.find_element_by_name("user").send_keys(user)
        driver.find_element_by_name("pwinput").send_keys(pwd)
        driver.find_element_by_name("submit").click()

        return output
