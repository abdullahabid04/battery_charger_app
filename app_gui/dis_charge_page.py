from UI_imports import Ui_discharge_form, Ui_back_ok_buttons_form
from app_gui.numpad import NumPad
from requirements import DIS_CHARGE


class DisChargePage(object):
    def __init__(self, workspace, buttons_space, btn_calls_func):
        self.workspace = workspace
        self.buttons_space = buttons_space
        self.btn_call = btn_calls_func

        self.dis_charge = Ui_discharge_form()
        self.buttons_back_ok = Ui_back_ok_buttons_form()

        self.num_pad = NumPad(self.workspace, self.buttons_space)

        self.dis_charge_values = ["", "", "", "", "", ]

    def set_up_ui(self):
        self.dis_charge.setupUi(self.workspace)
        self.dis_charge.win_discharge.show()

        self.buttons_back_ok.setupUi(self.buttons_space)
        self.buttons_back_ok.back_ok_buttons_win.show()

        self.set_button_calls()
        self.btn_call(DIS_CHARGE)

    def get_charge_config(self):
        if all(item != "" for item in self.dis_charge_values):
            return True, self.dis_charge_values
        else:
            return False, []

    def set_button_calls(self):
        self.dis_charge.set_dis_charge_current_btn_for_discharge.clicked.connect(
            self.goto_set_charge_current_for_dis_charge)
        self.dis_charge.set_dis_charge_time_btn_for_discharge.clicked.connect(
            self.goto_set_charge_time_for_dis_charge)
        self.dis_charge.set_dis_charge_voltage_btn_for_discharge.clicked.connect(
            self.goto_set_charge_voltage_for_dis_charge)
        self.dis_charge.set_optional_alerts_btn_for_discharge.clicked.connect(
            self.goto_set_optional_alerts_for_dis_charge)

    def open_num_pad(self):
        self.num_pad.set_up_ui()

    def goto_set_charge_current_for_dis_charge(self):
        self.open_num_pad()
        self.num_pad.buttons_cancel_ok.btn_ok_for_all.clicked.connect(
            self.get_back_from_set_charge_current_for_dis_charge)

    def goto_set_charge_time_for_dis_charge(self):
        self.open_num_pad()
        self.num_pad.buttons_cancel_ok.btn_ok_for_all.clicked.connect(
            self.get_back_from_set_charge_time_for_dis_charge)

    def goto_set_charge_voltage_for_dis_charge(self):
        self.open_num_pad()
        self.num_pad.buttons_cancel_ok.btn_ok_for_all.clicked.connect(
            self.get_back_from_set_charge_voltage_for_dis_charge)

    def goto_set_terminate_when_for_dis_charge(self):
        self.open_num_pad()
        self.num_pad.buttons_cancel_ok.btn_ok_for_all.clicked.connect(
            self.get_back_from_set_terminate_when_for_dis_charge)

    def goto_set_optional_alerts_for_dis_charge(self):
        self.open_num_pad()
        self.num_pad.buttons_cancel_ok.btn_ok_for_all.clicked.connect(
            self.get_back_from_set_optional_alerts_for_dis_charge)

    def get_back_from_set_charge_current_for_dis_charge(self):
        self.dis_charge_values[0] = self.num_pad.get_value()
        self.set_up_ui()
        self.set_dis_charge_values()

    def get_back_from_set_charge_time_for_dis_charge(self):
        self.dis_charge_values[1] = self.num_pad.get_value()
        self.set_up_ui()
        self.set_dis_charge_values()

    def get_back_from_set_charge_voltage_for_dis_charge(self):
        self.dis_charge_values[2] = self.num_pad.get_value()
        self.set_up_ui()
        self.set_dis_charge_values()

    def get_back_from_set_terminate_when_for_dis_charge(self):
        self.dis_charge_values[3] = self.num_pad.get_value()
        self.set_up_ui()
        self.set_dis_charge_values()

    def get_back_from_set_optional_alerts_for_dis_charge(self):
        self.dis_charge_values[4] = self.num_pad.get_value()
        self.set_up_ui()
        self.set_dis_charge_values()

    def set_dis_charge_values(self):
        self.dis_charge.set_dis_charge_current_for_discharge.setText(
            self.dis_charge_values[0])
        self.dis_charge.set_dis_charge_time_for_discharge.setText(
            self.dis_charge_values[1])
        self.dis_charge.set_dis_charge_volatge_for_discharge.setText(
            self.dis_charge_values[2])
        self.dis_charge.set_optional_alerts_for_discharge.setText(
            self.dis_charge_values[4])
