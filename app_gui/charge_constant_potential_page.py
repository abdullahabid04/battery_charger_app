from UI_imports import Ui_charge_constant_voltage_form, Ui_back_ok_buttons_form
from app_gui.numpad import NumPad
from requirements import CONSTANT_CHARGE_VOLTAGE


class ChargeConstantPotentialPage(object):
    def __init__(self, workspace, buttons_space, btn_calls_func):
        self.workspace = workspace
        self.buttons_space = buttons_space
        self.btn_call = btn_calls_func

        self.charge_constant_potential = Ui_charge_constant_voltage_form()
        self.buttons_back_ok = Ui_back_ok_buttons_form()

        self.num_pad = NumPad(self.workspace, self.buttons_space)

        self.constant_charge_potential_values = ["", "", "", "", ""]

    def set_up_ui(self):
        self.charge_constant_potential.setupUi(self.workspace)
        self.charge_constant_potential.win_charge_constant_voltage.show()

        self.buttons_back_ok.setupUi(self.buttons_space)
        self.buttons_back_ok.back_ok_buttons_win.show()

        self.set_button_calls()
        self.btn_call(CONSTANT_CHARGE_VOLTAGE)

    def get_charge_config(self):
        if all(item != "" for item in self.constant_charge_potential_values):
            return True, self.constant_charge_potential_values
        else:
            return False, []

    def set_button_calls(self):
        self.charge_constant_potential.set_charge_current_btn_for_charge_constant_voltage.clicked.connect(
            self.goto_set_charge_current_for_constant_charge_voltage)
        self.charge_constant_potential.set_charge_time_btn_for_charge_constant_voltage.clicked.connect(
            self.goto_set_charge_time_for_constant_charge_voltage)
        self.charge_constant_potential.set_charge_voltage_btn_for_charge_constant_voltage.clicked.connect(
            self.goto_set_charge_voltage_for_constant_charge_voltage)
        self.charge_constant_potential.set_optional_alerts_btn_for_charge_constant_voltage.clicked.connect(
            self.goto_set_optional_alerts_for_constant_charge_voltage)

    def open_num_pad(self):
        self.num_pad.set_up_ui()

    def goto_set_charge_current_for_constant_charge_voltage(self):
        self.open_num_pad()
        self.num_pad.buttons_cancel_ok.btn_ok_for_all.clicked.connect(
            self.get_back_from_set_charge_current_for_constant_charge_voltage)

    def goto_set_charge_time_for_constant_charge_voltage(self):
        self.open_num_pad()
        self.num_pad.buttons_cancel_ok.btn_ok_for_all.clicked.connect(
            self.get_back_from_set_charge_time_for_constant_charge_voltage)

    def goto_set_charge_voltage_for_constant_charge_voltage(self):
        self.open_num_pad()
        self.num_pad.buttons_cancel_ok.btn_ok_for_all.clicked.connect(
            self.get_back_from_set_charge_voltage_for_constant_charge_voltage)

    def goto_set_terminate_when_for_constant_charge_voltage(self):
        self.open_num_pad()
        self.num_pad.buttons_cancel_ok.btn_ok_for_all.clicked.connect(
            self.get_back_from_set_terminate_when_for_constant_charge_voltage)

    def goto_set_optional_alerts_for_constant_charge_voltage(self):
        self.open_num_pad()
        self.num_pad.buttons_cancel_ok.btn_ok_for_all.clicked.connect(
            self.get_back_from_set_optional_alerts_for_constant_charge_voltage)

    def get_back_from_set_charge_current_for_constant_charge_voltage(self):
        self.constant_charge_potential_values[0] = self.num_pad.get_value()
        self.set_up_ui()
        self.set_charge_constant_voltage_values()

    def get_back_from_set_charge_time_for_constant_charge_voltage(self):
        self.constant_charge_potential_values[1] = self.num_pad.get_value()
        self.set_up_ui()
        self.set_charge_constant_voltage_values()

    def get_back_from_set_charge_voltage_for_constant_charge_voltage(self):
        self.constant_charge_potential_values[2] = self.num_pad.get_value()
        self.set_up_ui()
        self.set_charge_constant_voltage_values()

    def get_back_from_set_terminate_when_for_constant_charge_voltage(self):
        self.constant_charge_potential_values[3] = self.num_pad.get_value()
        self.set_up_ui()
        self.set_charge_constant_voltage_values()

    def get_back_from_set_optional_alerts_for_constant_charge_voltage(self):
        self.constant_charge_potential_values[4] = self.num_pad.get_value()
        self.set_up_ui()
        self.set_charge_constant_voltage_values()

    def set_charge_constant_voltage_values(self):
        self.charge_constant_potential.set_charge_current_for_charge_constant_voltage.setText(
            self.constant_charge_potential_values[0])
        self.charge_constant_potential.set_charge_time_for_charge_constant_voltage.setText(
            self.constant_charge_potential_values[1])
        self.charge_constant_potential.set_charge_voltage_for_charge_constant_voltage.setText(
            self.constant_charge_potential_values[2])
        self.charge_constant_potential.set_optional_alerts_for_charge_constant_voltage.setText(
            self.constant_charge_potential_values[4])
