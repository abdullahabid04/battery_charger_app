from UI_imports import Ui_wait_win_form, Ui_back_ok_buttons_form
from requirements import WAIT_CHARGE


class WaitChargePage(object):
    def __init__(self, workspace, buttons_space, btn_calls_func):
        self.workspace = workspace
        self.buttons_space = buttons_space
        self.btn_call = btn_calls_func

        self.wait_charge = Ui_wait_win_form()
        self.buttons_back_ok = Ui_back_ok_buttons_form()

        self.wait_charge_values = ["", "", "", "", ""]

    def set_up_ui(self):
        self.wait_charge.setupUi(self.workspace)
        self.wait_charge.win_wait.show()

        self.buttons_back_ok.setupUi(self.buttons_space)
        self.buttons_back_ok.back_ok_buttons_win.show()

        self.btn_call(WAIT_CHARGE)

    def get_charge_config(self):
        if all(item != "" for item in self.wait_charge_values):
            return True, self.wait_charge_values
        else:
            return False, []
