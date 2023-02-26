import traceback

from UI_imports import Ui_main_home_page_form, Ui_logo_christie_form, Ui_view_programs_start_buttons_form
from app_gui.charge_constant_current_page import ChargeConstantCurrentPage
from app_gui.charge_constant_potential_page import ChargeConstantPotentialPage
from app_gui.reflex_charge_page import ReflexChargePage
from app_gui.dis_charge_page import DisChargePage
from app_gui.wait_charge_page import WaitChargePage
from app_gui.charging_screen import ChargingScreen
from requirements import CHARGE_TYPE_SELECTION, CONSTANT_CHARGE_CURRENT, CONSTANT_CHARGE_VOLTAGE, REFLEX_CHARGE, \
    DIS_CHARGE, WAIT_CHARGE


class HomePage(object):
    def __init__(self, frame):
        self.frame = frame

        self.home_page_ = Ui_main_home_page_form()
        self.christie_logo_ = Ui_logo_christie_form()
        self.buttons_view_programs_start_ = Ui_view_programs_start_buttons_form()

        self.charge_constant_current = None
        self.charge_constant_potential = None
        self.reflex_charge = None
        self.dis_charge = None
        self.wait_charge = None

        self.mode = None
        self.charge_config = None

    def set_up_ui(self):
        self.home_page_.setupUi(self.frame)
        self.christie_logo_.setupUi(self.home_page_.main_workspace)
        self.buttons_view_programs_start_.setupUi(self.home_page_.buttons_space)

        self.set_up_button_calls()

    def set_up_button_calls(self):
        self.home_page_.btn_charge_constant_current.clicked.connect(self.goto_charge_constant_current)
        self.home_page_.btn_charge_constant_voltage.clicked.connect(self.goto_charge_constant_potential)
        self.home_page_.btn_charge_reflex.clicked.connect(self.goto_reflex_charge)
        self.home_page_.btn_discharge.clicked.connect(self.goto_dis_charge)
        self.home_page_.btn_wait.clicked.connect(self.goto_wait_charge)

    def set_charge_btn_call(self, mode):
        for index, item in enumerate(CHARGE_TYPE_SELECTION):
            if mode is item:
                self.charge_config = [self.charge_constant_current,
                                      self.charge_constant_potential,
                                      self.reflex_charge,
                                      self.dis_charge,
                                      self.wait_charge, ][index].buttons_back_ok.btn_ok_for_all.clicked.connect(
                    self.start_charging)

    def goto_charge_constant_current(self):
        self.mode = CONSTANT_CHARGE_CURRENT

        self.charge_constant_current = ChargeConstantCurrentPage(self.home_page_.main_workspace,
                                                                 self.home_page_.buttons_space,
                                                                 self.set_charge_btn_call)

        self.charge_constant_current.set_up_ui()

        self.set_charge_btn_call(CONSTANT_CHARGE_CURRENT)

    def goto_charge_constant_potential(self):
        self.mode = CONSTANT_CHARGE_VOLTAGE

        self.charge_constant_potential = ChargeConstantPotentialPage(self.home_page_.main_workspace,
                                                                     self.home_page_.buttons_space,
                                                                     self.set_up_button_calls)

        self.charge_constant_potential.set_up_ui()

        self.set_charge_btn_call(CONSTANT_CHARGE_VOLTAGE)

    def goto_reflex_charge(self):
        self.mode = REFLEX_CHARGE

        self.reflex_charge = ReflexChargePage(self.home_page_.main_workspace, self.home_page_.buttons_space,
                                              self.set_up_button_calls)
        self.reflex_charge.set_up_ui()

        self.set_charge_btn_call(REFLEX_CHARGE)

    def goto_dis_charge(self):
        self.mode = DIS_CHARGE

        self.dis_charge = DisChargePage(self.home_page_.main_workspace, self.home_page_.buttons_space,
                                        self.set_up_button_calls)
        self.dis_charge.set_up_ui()

        self.set_charge_btn_call(DIS_CHARGE)

    def goto_wait_charge(self):
        self.mode = WAIT_CHARGE

        self.wait_charge = WaitChargePage(self.home_page_.main_workspace, self.home_page_.buttons_space,
                                          self.set_up_button_calls)
        self.wait_charge.set_up_ui()

        self.set_charge_btn_call(WAIT_CHARGE)

    def start_charging(self):
        for index, item in enumerate(CHARGE_TYPE_SELECTION):
            if self.mode is item:
                self.charge_config = [self.charge_constant_current,
                                      self.charge_constant_potential,
                                      self.reflex_charge,
                                      self.dis_charge,
                                      self.wait_charge, ][index].get_charge_config()[1]

        print(self.charge_config, self.mode)

        if all(item != "" for item in self.charge_config):
            try:
                charging_screen = ChargingScreen(self.home_page_.dashboard_main, self.home_page_.buttons_space,
                                                 self.charge_config, self.mode)
                charging_screen.set_up_ui()
                charging_screen.start_charging_process()
            except Exception as e:
                print(e)
                traceback.print_exc()
            finally:
                traceback.print_exc()
        else:
            pass
