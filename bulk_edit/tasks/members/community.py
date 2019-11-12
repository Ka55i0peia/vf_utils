from ..task_base import ComboboxChange
from selenium import webdriver


class ChangeUserClubProperty(ComboboxChange):

    def __init__(self, webdriver: webdriver, uid: int, flightClub: str, customPropertyNo: int = 1):
        '''
        `ui` user to edit
        `flightClub` custom property value to set (by string representation)
        '''
        self.uid = uid
        url = f"https://vereinsflieger.de/member/community/editfunctions.php?uid={uid}"
        super().__init__(webdriver=webdriver,
                         changeUrl=url,
                         cmbxTextValue=flightClub,
                         cmbxHtmlName=f"suc_prop_512_{customPropertyNo}")

    def ident(self) -> str:
        return f"Change user club uid='{self.uid}' to '{self.cmbxTextValue}'"


class ChangeUserStatus(ComboboxChange):

    def __init__(self, webdriver: webdriver, uid: int, statusName: str):
        '''
        `ui` user to edit
        `statusName` status to be set
        '''
        self.uid = uid
        url = f"https://vereinsflieger.de/member/community/editcommunity.php?uid={uid}"
        super().__init__(webdriver=webdriver,
                         changeUrl=url,
                         cmbxTextValue=statusName,
                         cmbxHtmlName=f"frm_msid")

    def ident(self) -> str:
        return f"Change user status uid='{self.uid}' to '{self.cmbxTextValue}'"
