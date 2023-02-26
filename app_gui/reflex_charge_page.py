from UI_imports import Ui_reflex_charge_form, Ui_back_ok_buttons_form
from app_gui.numpad import NumPad
from requirements import REFLEX_CHARGE


class ReflexChargePage(object):
    def __init__(self, workspace, buttons_space, btn_calls_func):
        self.workspace = workspace
        self.buttons_space = buttons_space
        self.btn_call = btn_calls_func

        self.reflex_charge = Ui_reflex_charge_form()
        self.buttons_back_ok = Ui_back_ok_buttons_form()

        self.num_pad = NumPad(self.workspace, self.buttons_space)

        self.reflex_charge_values = ["", "", "", "", ""]

    def set_up_ui(self):
        self.reflex_charge.setupUi(self.workspace)
        self.reflex_charge.win_reflex_charge.show()

        self.buttons_back_ok.setupUi(self.buttons_space)
        self.buttons_back_ok.back_ok_buttons_win.show()

        self.set_button_calls()
        self.btn_call(REFLEX_CHARGE)

    def get_charge_config(self):
        if all(item != "" for item in self.reflex_charge_values):
            return True, self.reflex_charge_values
        else:
            return False, []

    def set_button_calls(self):
        self.reflex_charge.set_charge_current_btn_for_reflex_charge.clicked.connect(
            self.goto_set_charge_current_for_reflex_charge)
        self.reflex_charge.set_charge_time_btn_for_reflex_charge.clicked.connect(
            self.goto_set_charge_time_for_reflex_charge)
        self.reflex_charge.set_charge_voltage_btn_for_reflex_charge.clicked.connect(
            self.goto_set_charge_voltage_for_reflex_charge)
        self.reflex_charge.set_reflex_type_A_for_reflex_charge.clicked.connect(
            self.goto_set_reflex_type_a_for_constant_charge_current)
        self.reflex_charge.set_reflex_type_B_for_reflex_charge.clicked.connect(
            self.goto_set_reflex_type_b_for_constant_charge_current)
        self.reflex_charge.set_optional_alerts_btn_for_reflex_charge.clicked.connect(
            self.goto_set_optional_alerts_for_reflex_charge)

    def open_num_pad(self):
        self.num_pad.set_up_ui()

    def goto_set_charge_current_for_reflex_charge(self):
        self.open_num_pad()
        self.num_pad.buttons_cancel_ok.btn_ok_for_all.clicked.connect(
            self.get_back_from_set_charge_current_for_reflex_charge)

    def goto_set_charge_time_for_reflex_charge(self):
        self.open_num_pad()
        self.num_pad.buttons_cancel_ok.btn_ok_for_all.clicked.connect(
            self.get_back_from_set_charge_time_for_reflex_charge)

    def goto_set_charge_voltage_for_reflex_charge(self):
        self.open_num_pad()
        self.num_pad.buttons_cancel_ok.btn_ok_for_all.clicked.connect(
            self.get_back_from_set_charge_voltage_for_reflex_charge)

    def goto_set_terminate_when_for_reflex_charge(self):
        self.open_num_pad()
        self.num_pad.buttons_cancel_ok.btn_ok_for_all.clicked.connect(
            self.get_back_from_set_terminate_when_for_reflex_charge)

    def goto_set_reflex_type_a_for_constant_charge_current(self):
        self.reflex_charge_values[3] = "A"

    def goto_set_reflex_type_b_for_constant_charge_current(self):
        self.reflex_charge_values[3] = "B"

    def goto_set_optional_alerts_for_reflex_charge(self):
        self.open_num_pad()
        self.num_pad.buttons_cancel_ok.btn_ok_for_all.clicked.connect(
            self.get_back_from_set_optional_alerts_for_reflex_charge)

    def get_back_from_set_charge_current_for_reflex_charge(self):
        self.reflex_charge_values[0] = self.num_pad.get_value()
        self.set_up_ui()
        self.set_reflex_charge_values()

    def get_back_from_set_charge_time_for_reflex_charge(self):
        self.reflex_charge_values[1] = self.num_pad.get_value()
        self.set_up_ui()
        self.set_reflex_charge_values()

    def get_back_from_set_charge_voltage_for_reflex_charge(self):
        self.reflex_charge_values[2] = self.num_pad.get_value()
        self.set_up_ui()
        self.set_reflex_charge_values()

    def get_back_from_set_terminate_when_for_reflex_charge(self):
        self.reflex_charge_values[3] = self.num_pad.get_value()
        self.set_up_ui()
        self.set_reflex_charge_values()

    def get_back_from_set_optional_alerts_for_reflex_charge(self):
        self.reflex_charge_values[4] = self.num_pad.get_value()
        self.set_up_ui()
        self.set_reflex_charge_values()

    def set_reflex_charge_values(self):
        self.reflex_charge.set_charge_current_for_reflex_charge.setText(
            self.reflex_charge_values[0])
        self.reflex_charge.set_charge_time_for_reflex_charge.setText(
            self.reflex_charge_values[1])
        self.reflex_charge.set_charge_volatge_for_reflex_charge.setText(
            self.reflex_charge_values[2])

        if self.reflex_charge_values[3] == "":
            pass
        else:
            if self.reflex_charge_values[3] == "A":
                self.reflex_charge.set_reflex_type_A_for_reflex_charge.setChecked(True)
            elif self.reflex_charge_values[3] == "B":
                self.reflex_charge.set_reflex_type_B_for_reflex_charge.setChecked(True)
            else:
                pass

        self.reflex_charge.set_optional_alerts_for_reflex_charge.setText(
            self.reflex_charge_values[4])
