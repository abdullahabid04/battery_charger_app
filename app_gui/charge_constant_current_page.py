from UI_imports import Ui_charge_constant_current_form, Ui_back_ok_buttons_form
from app_gui.numpad import NumPad
from requirements import CONSTANT_CHARGE_CURRENT


class ChargeConstantCurrentPage(object):
    def __init__(self, workspace, buttons_space, btn_calls_func):
        self.workspace = workspace
        self.buttons_space = buttons_space
        self.btn_calls = btn_calls_func

        self.charge_constant_current = Ui_charge_constant_current_form()
        self.buttons_back_ok = Ui_back_ok_buttons_form()

        self.num_pad = NumPad(self.workspace, self.buttons_space)

        self.constant_charge_current_values = ["", "", "", "", ""]

    def set_up_ui(self):
        self.charge_constant_current.setupUi(self.workspace)
        self.charge_constant_current.win_charge_constant_current.show()

        self.buttons_back_ok.setupUi(self.buttons_space)
        self.buttons_back_ok.back_ok_buttons_win.show()

        self.set_button_calls()
        self.btn_calls(CONSTANT_CHARGE_CURRENT)

    def get_charge_config(self):
        if all(item != "" for item in self.constant_charge_current_values):
            return True, self.constant_charge_current_values
        else:
            return False, []

    def set_button_calls(self):
        self.charge_constant_current.set_charge_current_btn_for_charge_constant_current.clicked.connect(
            self.goto_set_charge_current_for_constant_charge_current)
        self.charge_constant_current.set_charge_time_btn_for_charge_constant_current.clicked.connect(
            self.goto_set_charge_time_for_constant_charge_current)
        self.charge_constant_current.set_charge_voltage_btn_for_charge_constant_current.clicked.connect(
            self.goto_set_charge_voltage_for_constant_charge_current)
        self.charge_constant_current.terminate_on_time_for_charge_constant_current.clicked.connect(
            self.goto_set_terminate_on_one_for_constant_charge_current)
        self.charge_constant_current.terminate_on_voltage_for_charge_constant_current.clicked.connect(
            self.goto_set_terminate_on_both_for_constant_charge_current)
        self.charge_constant_current.set_optional_alerts_btn_for_charge_constant_current.clicked.connect(
            self.goto_set_optional_alerts_for_constant_charge_current)

    def open_num_pad(self):
        self.num_pad.set_up_ui()

    def goto_set_charge_current_for_constant_charge_current(self):
        self.open_num_pad()
        self.num_pad.buttons_cancel_ok.btn_ok_for_all.clicked.connect(
            self.get_back_from_set_charge_current_for_constant_charge_current)

    def goto_set_charge_time_for_constant_charge_current(self):
        self.open_num_pad()
        self.num_pad.buttons_cancel_ok.btn_ok_for_all.clicked.connect(
            self.get_back_from_set_charge_time_for_constant_charge_current)

    def goto_set_charge_voltage_for_constant_charge_current(self):
        self.open_num_pad()
        self.num_pad.buttons_cancel_ok.btn_ok_for_all.clicked.connect(
            self.get_back_from_set_charge_voltage_for_constant_charge_current)

    def goto_set_terminate_when_for_constant_charge_current(self):
        self.open_num_pad()
        self.num_pad.buttons_cancel_ok.btn_ok_for_all.clicked.connect(
            self.get_back_from_set_terminate_when_for_constant_charge_current)

    def goto_set_optional_alerts_for_constant_charge_current(self):
        self.open_num_pad()
        self.num_pad.buttons_cancel_ok.btn_ok_for_all.clicked.connect(
            self.get_back_from_set_optional_alerts_for_constant_charge_current)

    def goto_set_terminate_on_one_for_constant_charge_current(self):
        self.constant_charge_current_values[3] = "OR"

    def goto_set_terminate_on_both_for_constant_charge_current(self):
        self.constant_charge_current_values[3] = "AND"

    def get_back_from_set_charge_current_for_constant_charge_current(self):
        self.constant_charge_current_values[0] = self.num_pad.get_value()
        self.set_up_ui()
        self.set_charge_constant_current_values()

    def get_back_from_set_charge_time_for_constant_charge_current(self):
        self.constant_charge_current_values[1] = self.num_pad.get_value()
        self.set_up_ui()
        self.set_charge_constant_current_values()

    def get_back_from_set_charge_voltage_for_constant_charge_current(self):
        self.constant_charge_current_values[2] = self.num_pad.get_value()
        self.set_up_ui()
        self.set_charge_constant_current_values()

    def get_back_from_set_terminate_when_for_constant_charge_current(self):
        self.constant_charge_current_values[3] = self.num_pad.get_value()
        self.set_up_ui()
        self.set_charge_constant_current_values()

    def get_back_from_set_optional_alerts_for_constant_charge_current(self):
        self.constant_charge_current_values[4] = self.num_pad.get_value()
        self.set_up_ui()
        self.set_charge_constant_current_values()

    def set_charge_constant_current_values(self):
        self.charge_constant_current.set_current_for_charge_constant_current.setText(
            self.constant_charge_current_values[0])
        self.charge_constant_current.set_time_for_charge_constant_current.setText(
            self.constant_charge_current_values[1])
        self.charge_constant_current.set_voltage_for_charge_constant_current.setText(
            self.constant_charge_current_values[2])

        if self.constant_charge_current_values[3] == "":
            pass
        else:
            if self.constant_charge_current_values[3] == "OR":
                self.charge_constant_current.terminate_on_time_for_charge_constant_current.setChecked(True)
            elif self.constant_charge_current_values[3] == "AND":
                self.charge_constant_current.terminate_on_voltage_for_charge_constant_current.setChecked(True)
            else:
                pass

        self.charge_constant_current.set_optional_alerts_for_charge_constant_current.setText(
            self.constant_charge_current_values[4])
