from ..task_base import ComboboxChange, Task
from selenium import webdriver


class ChangeUserClubProperty(ComboboxChange):

    def __init__(self, flightClub: str, customPropertyNo: int = 1):
        '''
        `ui` user to edit
        `flightClub` custom property value to set (by string representation)
        '''
        super().__init__(cmbxTextValue=flightClub,
                         cmbxHtmlName=f"suc_prop_512_{customPropertyNo}")

    def ident(self) -> str:
        return f"Change user club"

    def execute(self, input: dict) -> Union[TaskOutput, Iterable[TaskOutput]]:
        uid = self.get_parameter(input, "uid")
        url = f"https://vereinsflieger.de/member/community/editfunctions.php?uid={uid}"
        input["url"] = url
        return super().execute(input)


class ChangeUserStatus(ComboboxChange):

    def __init__(self, statusName: str):
        '''
        `ui` user to edit
        `statusName` status to be set
        '''
        super().__init__(cmbxTextValue=statusName,
                         cmbxHtmlName=f"frm_msid")

    def ident(self) -> str:
        return f"Change user status"

    def execute(self, input: dict) -> Union[TaskOutput, Iterable[TaskOutput]]:
        uid = self.get_parameter(input, "uid")
        url = f"https://vereinsflieger.de/member/community/editcommunity.php?uid={uid}"
        input["url"] = url
        return super().execute(input)
