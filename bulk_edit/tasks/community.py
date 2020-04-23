from .task_base import ComboboxChange, Task
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from typing import List


class ChangeUserClubProperty(ComboboxChange):

    def __init__(self, driver: webdriver, uid: int, flightClub: str, customPropertyNo: int = 1):
        '''
        `ui` user to edit
        `flightClub` custom property value to set (by string representation)
        '''
        self.uid = uid
        url = f"https://vereinsflieger.de/member/community/editfunctions.php?uid={uid}"
        super().__init__(driver=driver,
                         changeUrl=url,
                         cmbxTextValue=flightClub,
                         cmbxHtmlName=f"suc_prop_512_{customPropertyNo}")

    def ident(self) -> str:
        return f"Change user club (uid='{self.uid}') to '{self.cmbxTextValue}'"

    @classmethod
    def parameters(self) -> List[str]:
        return ['uid', 'flightClub', 'customPropertyNo']


class ChangeUserStatus(ComboboxChange):

    def __init__(self, driver: webdriver, uid: int, statusName: str):
        '''
        `ui` user to edit
        `statusName` status to be set
        '''
        self.uid = uid
        url = f"https://vereinsflieger.de/member/community/editcommunity.php?uid={uid}"
        super().__init__(driver=driver,
                         changeUrl=url,
                         cmbxTextValue=statusName,
                         cmbxHtmlName=f"frm_msid")

    def ident(self) -> str:
        return f"Change user status (uid='{self.uid}') to '{self.cmbxTextValue}'"

    @classmethod
    def parameters(self) -> List[str]:
        return ['uid', 'statusName']


class AddCommunityCosts(Task):

    def __init__(self, driver: webdriver, uid: int, costType: str,
                 comment: str, validFrom: str, validTo: str):
        '''
        GUI item: Gebühren -> Neuer Datensatz
        '''
        self.driver = driver
        self.url = f"https://vereinsflieger.de/member/community/editcommunitycost.php?uid={uid}"

        self.uid = uid
        self.costType = costType
        self.comment = comment
        self.validFrom = validFrom
        self.validTo = validTo

    @classmethod
    def parameters(self) -> List[str]:
        return ['uid', 'costType', 'comment', 'validFrom', 'validTo']

    def execute(self) -> bool:
        driver = self.driver

        # open webpage
        driver.get(self.url)

        newCostButton = driver.find_element_by_id('TlbItem1')
        newCostButton.click()

        costType = driver.find_element_by_name('frm_ctid')
        selector = Select(costType)
        selector.select_by_visible_text(self.costType)

        comment = driver.find_element_by_name('frm_comment')
        comment.send_keys(self.comment)

        validFrom = driver.find_element_by_name('frm_validfrom')
        validFrom.clear()
        validFrom.send_keys(self.validFrom)

        validTo = driver.find_element_by_name('frm_validto')
        validTo.send_keys(self.validTo)

        costType.submit()

        # TODO implement a checker for valid input (may make use of JS function: checkMandatory())
        return True

    def ident(self) -> str:
        return f"AddCommunityCosts for user {self.uid}"
