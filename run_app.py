from PyQt5.QtCore import *
import functools
import time
import datetime
import asyncio
from UI_imports import *
from requirements import *
from table_view_data_model import TableModel
from background_workers import Worker
from rpi_arduino_i2c_comm import write_data_to_arduino, read_data_from_arduino


class App(object):
    def __init__(self, window):
        self.win = window

        self.timer = QTimer()
        self.threadpool = QThreadPool()

        self.home_page_ = Ui_main_home_page_form()
        self.christie_logo_ = Ui_logo_christie_form()
        self.charging_status_ = Ui_charging_status_form()
        self.charge_constant_current_ = Ui_charge_constant_current_form()
        self.charge_constant_voltage_ = Ui_charge_constant_voltage_form()
        self.reflex_charge_ = Ui_reflex_charge_form()
        self.discharge_ = Ui_discharge_form()
        self.wait_ = Ui_wait_win_form()
        self.current_programs_ = Ui_current_programs_form()
        self.all_programs_ = Ui_all_programs_form()
        self.all_views_ = Ui_all_views_form()
        self.num_pad_ = Ui_number_pad_form()
        self.buttons_back_ok_ = Ui_back_ok_buttons_form()
        self.buttons_cancel_ok_ = Ui_cancel_ok_buttons_form()
        self.buttons_view_programs_start_ = Ui_view_programs_start_buttons_form()
        self.buttons_stop_next_pause_ = Ui_stop_next_pause_buttons_form()

        self.constant_charge_current_values = ["", "", "", "0", "", ]
        self.constant_charge_voltage_values = ["", "", "", "0", "", ]
        self.reflex_charge_values = ["", "", "", "0", "", ]
        self.dis_charge_values = ["", "", "", "0", "", ]
        self.wait_values = ["", "", "", "0", "", ]

        self.charging_info = []
        self.selected_charging_mode = ""
        self.running = False

        self.all_charging_modes_values = [self.constant_charge_current_values, self.constant_charge_voltage_values,
                                          self.reflex_charge_values, self.dis_charge_values, self.wait_values]

    def run(self):
        self.open_home_page()
        self.win.show()

    def open_home_page(self):
        self.home_page_.setupUi(self.win)
        self.christie_logo_.setupUi(self.home_page_.main_workspace)
        self.buttons_view_programs_start_.setupUi(self.home_page_.buttons_space)

        self.home_page_.btn_charge_constant_current.clicked.connect(self.goto_constant_charge_current)
        self.home_page_.btn_charge_constant_voltage.clicked.connect(self.goto_constant_charge_voltage)
        self.home_page_.btn_charge_reflex.clicked.connect(self.goto_reflex_charge)
        self.home_page_.btn_discharge.clicked.connect(self.goto_discharge)
        self.home_page_.btn_wait.clicked.connect(self.goto_wait)

        self.buttons_view_programs_start_.btn_view_settings_home.clicked.connect(self.show_all_views_page)
        self.buttons_view_programs_start_.btn_programs_settings_home.clicked.connect(self.show_all_programs_page)

    def goto_home_page(self):
        self.christie_logo_.setupUi(self.home_page_.main_workspace)
        self.christie_logo_.win_christie_logo.show()
        self.buttons_view_programs_start_.setupUi(self.home_page_.buttons_space)
        self.buttons_view_programs_start_.view_programs_start_buttons_win.show()

        self.buttons_view_programs_start_.btn_view_settings_home.clicked.connect(self.show_all_views_page)
        self.buttons_view_programs_start_.btn_programs_settings_home.clicked.connect(self.show_all_programs_page)

    def set_values_for_start_charging(self):
        for index, mode in enumerate(CHARGE_TYPE_SELECTION):
            if self.selected_charging_mode == mode:
                self.charging_info = self.all_charging_modes_values[index]

    def goto_start_charging_page(self):
        self.set_values_for_start_charging()

        validate_all_values = False

        if self.selected_charging_mode == CONSTANT_CHARGE_CURRENT:
            validate_all_values = all(item != "" for item in self.charging_info)
        elif self.selected_charging_mode == CONSTANT_CHARGE_VOLTAGE:
            validate_all_values = all(item != "" for item in self.charging_info)
        elif self.selected_charging_mode == REFLEX_CHARGE:
            validate_all_values = all(item != "" for item in self.charging_info)
        elif self.selected_charging_mode == DIS_CHARGE:
            validate_all_values = all(item != "" for item in self.charging_info)
        elif self.selected_charging_mode == WAIT_CHARGE:
            validate_all_values = all(item != "" for item in self.charging_info)
        else:
            pass

        if validate_all_values:
            self.running = True
            self.start_charging_process()
            print(self.charging_info)
        else:
            pass

    def start_charging_process(self):
        self.charging_status_.setupUi(self.home_page_.dashboard_main)
        self.charging_status_.win_charging_status.show()
        self.buttons_stop_next_pause_.setupUi(self.home_page_.buttons_space)
        self.buttons_stop_next_pause_.stop_next_pause_buttons_win.show()

        self.charging_status_.charge_current_display.display(self.charging_info[0])
        self.charging_status_.remaining_time.setText(self.charging_info[1])
        self.charging_status_.charge_voltage_display.display(self.charging_info[2])
        self.charging_status_.view_charge_type.setText(self.selected_charging_mode)

        table_model = TableModel(data=[self.charging_info])
        self.charging_status_.show_charge_info.setModel(table_model)

        self.start_i2c_comm_worker()
        self.start_count_down_timer_worker()

    def start_count_down_timer_worker(self):
        timer_worker = Worker(self.start_count_down_timer)
        self.threadpool.start(timer_worker)

    def start_count_down_timer(self):
        date = datetime.date.today()
        hour, minute, second = str(self.charging_info[1]).split(':')
        hour, minute, second = int(hour), int(minute), int(second)
        year, month, day = date.year, date.month, date.day

        date_time_ = datetime.datetime(year=year, month=month, day=day, hour=hour, minute=minute, second=second)
        date_time_delta = datetime.timedelta(seconds=1)

        while self.running:
            date_, time_ = str(date_time_).split(' ')
            self.charging_status_.remaining_time.setText(time_)
            print(date_, time_)
            time.sleep(1)
            date_time_ = date_time_ - date_time_delta

    def start_i2c_comm_worker(self):
        i2c_comm_worker = Worker(self.process_i2c_comm)
        self.threadpool.start(i2c_comm_worker)

    def process_i2c_comm(self):
        asyncio.run(self.start_i2c_comm())

    async def start_i2c_comm(self):
        while self.running:
            i2c_write_task = asyncio.create_task(write_data_to_arduino())
            i2c_write_task_value = await i2c_write_task

            i2c_read_task = asyncio.create_task(read_data_from_arduino())
            i2c_read_task_value = await i2c_read_task

    def show_all_programs_page(self):
        self.all_programs_.setupUi(self.home_page_.main_workspace)
        self.all_programs_.win_all_programs.show()

        self.setup_back_ok_buttons()

    def show_all_views_page(self):
        self.all_views_.setupUi(self.home_page_.main_workspace)
        self.all_views_.win_all_views.show()

        self.setup_back_ok_buttons()

    def setup_back_ok_buttons(self):
        self.buttons_back_ok_.setupUi(self.home_page_.buttons_space)
        self.buttons_back_ok_.back_ok_buttons_win.show()

        self.buttons_back_ok_.btn_ok_for_all.clicked.connect(self.goto_start_charging_page)
        self.buttons_back_ok_.btn_back_for_all.clicked.connect(self.goto_home_page)

    def goto_constant_charge_current(self):
        self.selected_charging_mode = CONSTANT_CHARGE_CURRENT

        self.charge_constant_current_.setupUi(self.home_page_.main_workspace)
        self.charge_constant_current_.win_charge_constant_current.show()

        self.setup_back_ok_buttons()

        self.charge_constant_current_.set_charge_current_btn_for_charge_constant_current.clicked.connect(
            self.goto_set_charge_current_for_constant_charge_current)
        self.charge_constant_current_.set_charge_time_btn_for_charge_constant_current.clicked.connect(
            self.goto_set_charge_time_for_constant_charge_current)
        self.charge_constant_current_.set_charge_voltage_btn_for_charge_constant_current.clicked.connect(
            self.goto_set_charge_voltage_for_constant_charge_current)
        self.charge_constant_current_.terminate_on_time_for_charge_constant_current.clicked.connect(
            self.goto_set_terminate_on_one_for_constant_charge_current)
        self.charge_constant_current_.terminate_on_voltage_for_charge_constant_current.clicked.connect(
            self.goto_set_terminate_on_both_for_constant_charge_current)
        self.charge_constant_current_.set_optional_alerts_btn_for_charge_constant_current.clicked.connect(
            self.goto_set_optional_alerts_for_constant_charge_current)

    def goto_constant_charge_voltage(self):
        self.selected_charging_mode = CONSTANT_CHARGE_VOLTAGE

        self.charge_constant_voltage_.setupUi(self.home_page_.main_workspace)
        self.charge_constant_voltage_.win_charge_constant_voltage.show()

        self.setup_back_ok_buttons()

        self.charge_constant_voltage_.set_charge_current_btn_for_charge_constant_voltage.clicked.connect(
            self.goto_set_charge_current_for_constant_charge_voltage)
        self.charge_constant_voltage_.set_charge_time_btn_for_charge_constant_voltage.clicked.connect(
            self.goto_set_charge_time_for_constant_charge_voltage)
        self.charge_constant_voltage_.set_charge_voltage_btn_for_charge_constant_voltage.clicked.connect(
            self.goto_set_charge_voltage_for_constant_charge_voltage)
        self.charge_constant_voltage_.set_optional_alerts_btn_for_charge_constant_voltage.clicked.connect(
            self.goto_set_optional_alerts_for_constant_charge_voltage)

    def goto_reflex_charge(self):
        self.selected_charging_mode = REFLEX_CHARGE

        self.reflex_charge_.setupUi(self.home_page_.main_workspace)
        self.reflex_charge_.win_reflex_charge.show()

        self.setup_back_ok_buttons()

        self.reflex_charge_.set_charge_current_btn_for_reflex_charge.clicked.connect(
            self.goto_set_charge_current_for_reflex_charge)
        self.reflex_charge_.set_charge_time_btn_for_reflex_charge.clicked.connect(
            self.goto_set_charge_time_for_reflex_charge)
        self.reflex_charge_.set_charge_voltage_btn_for_reflex_charge.clicked.connect(
            self.goto_set_charge_voltage_for_reflex_charge)
        self.reflex_charge_.set_reflex_type_A_for_reflex_charge.clicked.connect(
            self.goto_set_reflex_type_a_for_constant_charge_current)
        self.reflex_charge_.set_reflex_type_B_for_reflex_charge.clicked.connect(
            self.goto_set_reflex_type_b_for_constant_charge_current)
        self.reflex_charge_.set_optional_alerts_btn_for_reflex_charge.clicked.connect(
            self.goto_set_optional_alerts_for_reflex_charge)

    def goto_discharge(self):
        self.selected_charging_mode = DIS_CHARGE

        self.discharge_.setupUi(self.home_page_.main_workspace)
        self.discharge_.win_discharge.show()

        self.setup_back_ok_buttons()

        self.discharge_.set_dis_charge_current_btn_for_discharge.clicked.connect(
            self.goto_set_charge_current_for_dis_charge)
        self.discharge_.set_dis_charge_time_btn_for_discharge.clicked.connect(
            self.goto_set_charge_time_for_dis_charge)
        self.discharge_.set_dis_charge_voltage_btn_for_discharge.clicked.connect(
            self.goto_set_charge_voltage_for_dis_charge)
        self.discharge_.set_optional_alerts_btn_for_discharge.clicked.connect(
            self.goto_set_optional_alerts_for_dis_charge)

    def goto_wait(self):
        self.selected_charging_mode = WAIT_CHARGE

        self.wait_.setupUi(self.home_page_.main_workspace)
        self.wait_.win_wait.show()

        self.setup_back_ok_buttons()

    def open_num_pad(self):
        self.num_pad_.setupUi(self.home_page_.main_workspace)
        self.num_pad_.win_number_pad.show()
        self.buttons_cancel_ok_.setupUi(self.home_page_.buttons_space)
        self.buttons_cancel_ok_.cancel_ok_buttons_win.show()

        btn_num_pad = [self.num_pad_.btn_1_num_pad, self.num_pad_.btn_2_num_pad, self.num_pad_.btn_3_num_pad,
                       self.num_pad_.btn_4_num_pad, self.num_pad_.btn_5_num_pad, self.num_pad_.btn_6_num_pad,
                       self.num_pad_.btn_7_num_pad, self.num_pad_.btn_8_num_pad, self.num_pad_.btn_9_num_pad,
                       self.num_pad_.btn_semi_colon_num_pad, self.num_pad_.btn_0_num_pad,
                       self.num_pad_.btn_dot_num_pad, ]

        self.num_pad_.delete_input_value.clicked.connect(self.backspace_for_num_pad_input)

        for index, btn in enumerate(btn_num_pad):
            btn.clicked.connect(
                functools.partial(self.set_input_value_to_text_field, "{}".format(LABELS_OF_BUTTONS[index])))

    def set_input_value_to_text_field(self, value):
        old_value = self.num_pad_.num_pad_input_value.text()
        new_value = old_value + value

        self.num_pad_.num_pad_input_value.setText(new_value)

    def backspace_for_num_pad_input(self):
        text = self.num_pad_.num_pad_input_value.text()
        if len(text) == 0:
            pass
        else:
            new_text = text[:-1]
            self.num_pad_.num_pad_input_value.setText(new_text)

    def goto_set_charge_current_for_constant_charge_current(self):
        self.open_num_pad()
        self.buttons_cancel_ok_.btn_ok_for_all.clicked.connect(
            self.get_back_from_set_charge_current_for_constant_charge_current)

    def goto_set_charge_time_for_constant_charge_current(self):
        self.open_num_pad()
        self.buttons_cancel_ok_.btn_ok_for_all.clicked.connect(
            self.get_back_from_set_charge_time_for_constant_charge_current)

    def goto_set_charge_voltage_for_constant_charge_current(self):
        self.open_num_pad()
        self.buttons_cancel_ok_.btn_ok_for_all.clicked.connect(
            self.get_back_from_set_charge_voltage_for_constant_charge_current)

    def goto_set_terminate_when_for_constant_charge_current(self):
        self.open_num_pad()
        self.buttons_cancel_ok_.btn_ok_for_all.clicked.connect(
            self.get_back_from_set_terminate_when_for_constant_charge_current)

    def goto_set_optional_alerts_for_constant_charge_current(self):
        self.open_num_pad()
        self.buttons_cancel_ok_.btn_ok_for_all.clicked.connect(
            self.get_back_from_set_optional_alerts_for_constant_charge_current)

    def goto_set_terminate_on_one_for_constant_charge_current(self):
        self.constant_charge_current_values[3] = "OR"

    def goto_set_terminate_on_both_for_constant_charge_current(self):
        self.constant_charge_current_values[3] = "AND"

    def get_back_from_set_charge_current_for_constant_charge_current(self):
        self.constant_charge_current_values[0] = self.num_pad_.num_pad_input_value.text()
        self.goto_constant_charge_current()
        self.set_charge_constant_current_values()

    def get_back_from_set_charge_time_for_constant_charge_current(self):
        self.constant_charge_current_values[1] = self.num_pad_.num_pad_input_value.text()
        self.goto_constant_charge_current()
        self.set_charge_constant_current_values()

    def get_back_from_set_charge_voltage_for_constant_charge_current(self):
        self.constant_charge_current_values[2] = self.num_pad_.num_pad_input_value.text()
        self.goto_constant_charge_current()
        self.set_charge_constant_current_values()

    def get_back_from_set_terminate_when_for_constant_charge_current(self):
        self.constant_charge_current_values[3] = self.num_pad_.num_pad_input_value.text()
        self.goto_constant_charge_current()
        self.set_charge_constant_current_values()

    def get_back_from_set_optional_alerts_for_constant_charge_current(self):
        self.constant_charge_current_values[4] = self.num_pad_.num_pad_input_value.text()
        self.goto_constant_charge_current()
        self.set_charge_constant_current_values()

    def set_charge_constant_current_values(self):
        self.charge_constant_current_.set_current_for_charge_constant_current.setText(
            self.constant_charge_current_values[0])
        self.charge_constant_current_.set_time_for_charge_constant_current.setText(
            self.constant_charge_current_values[1])
        self.charge_constant_current_.set_voltage_for_charge_constant_current.setText(
            self.constant_charge_current_values[2])

        if self.constant_charge_current_values[3] == "":
            pass
        else:
            if self.constant_charge_current_values[3] == "OR":
                self.charge_constant_current_.terminate_on_time_for_charge_constant_current.setChecked(True)
            elif self.constant_charge_current_values[3] == "AND":
                self.charge_constant_current_.terminate_on_voltage_for_charge_constant_current.setChecked(True)
            else:
                pass

        self.charge_constant_current_.set_optional_alerts_for_charge_constant_current.setText(
            self.constant_charge_current_values[4])

    def goto_set_charge_current_for_constant_charge_voltage(self):
        self.open_num_pad()
        self.buttons_cancel_ok_.btn_ok_for_all.clicked.connect(
            self.get_back_from_set_charge_current_for_constant_charge_voltage)

    def goto_set_charge_time_for_constant_charge_voltage(self):
        self.open_num_pad()
        self.buttons_cancel_ok_.btn_ok_for_all.clicked.connect(
            self.get_back_from_set_charge_time_for_constant_charge_voltage)

    def goto_set_charge_voltage_for_constant_charge_voltage(self):
        self.open_num_pad()
        self.buttons_cancel_ok_.btn_ok_for_all.clicked.connect(
            self.get_back_from_set_charge_voltage_for_constant_charge_voltage)

    def goto_set_terminate_when_for_constant_charge_voltage(self):
        self.open_num_pad()
        self.buttons_cancel_ok_.btn_ok_for_all.clicked.connect(
            self.get_back_from_set_terminate_when_for_constant_charge_voltage)

    def goto_set_optional_alerts_for_constant_charge_voltage(self):
        self.open_num_pad()
        self.buttons_cancel_ok_.btn_ok_for_all.clicked.connect(
            self.get_back_from_set_optional_alerts_for_constant_charge_voltage)

    def get_back_from_set_charge_current_for_constant_charge_voltage(self):
        self.constant_charge_voltage_values[0] = self.num_pad_.num_pad_input_value.text()
        self.goto_constant_charge_voltage()
        self.set_charge_constant_voltage_values()

    def get_back_from_set_charge_time_for_constant_charge_voltage(self):
        self.constant_charge_voltage_values[1] = self.num_pad_.num_pad_input_value.text()
        self.goto_constant_charge_voltage()
        self.set_charge_constant_voltage_values()

    def get_back_from_set_charge_voltage_for_constant_charge_voltage(self):
        self.constant_charge_voltage_values[2] = self.num_pad_.num_pad_input_value.text()
        self.goto_constant_charge_voltage()
        self.set_charge_constant_voltage_values()

    def get_back_from_set_terminate_when_for_constant_charge_voltage(self):
        self.constant_charge_voltage_values[3] = self.num_pad_.num_pad_input_value.text()
        self.goto_constant_charge_voltage()
        self.set_charge_constant_voltage_values()

    def get_back_from_set_optional_alerts_for_constant_charge_voltage(self):
        self.constant_charge_voltage_values[4] = self.num_pad_.num_pad_input_value.text()
        self.goto_constant_charge_voltage()
        self.set_charge_constant_voltage_values()

    def set_charge_constant_voltage_values(self):
        self.charge_constant_voltage_.set_charge_current_for_charge_constant_voltage.setText(
            self.constant_charge_voltage_values[0])
        self.charge_constant_voltage_.set_charge_time_for_charge_constant_voltage.setText(
            self.constant_charge_voltage_values[1])
        self.charge_constant_voltage_.set_charge_voltage_for_charge_constant_voltage.setText(
            self.constant_charge_voltage_values[2])
        self.charge_constant_voltage_.set_optional_alerts_for_charge_constant_voltage.setText(
            self.constant_charge_voltage_values[4])

    def goto_set_charge_current_for_reflex_charge(self):
        self.open_num_pad()
        self.buttons_cancel_ok_.btn_ok_for_all.clicked.connect(
            self.get_back_from_set_charge_current_for_reflex_charge)

    def goto_set_charge_time_for_reflex_charge(self):
        self.open_num_pad()
        self.buttons_cancel_ok_.btn_ok_for_all.clicked.connect(
            self.get_back_from_set_charge_time_for_reflex_charge)

    def goto_set_charge_voltage_for_reflex_charge(self):
        self.open_num_pad()
        self.buttons_cancel_ok_.btn_ok_for_all.clicked.connect(
            self.get_back_from_set_charge_voltage_for_reflex_charge)

    def goto_set_terminate_when_for_reflex_charge(self):
        self.open_num_pad()
        self.buttons_cancel_ok_.btn_ok_for_all.clicked.connect(
            self.get_back_from_set_terminate_when_for_reflex_charge)

    def goto_set_reflex_type_a_for_constant_charge_current(self):
        self.reflex_charge_values[3] = "A"

    def goto_set_reflex_type_b_for_constant_charge_current(self):
        self.reflex_charge_values[3] = "B"

    def goto_set_optional_alerts_for_reflex_charge(self):
        self.open_num_pad()
        self.buttons_cancel_ok_.btn_ok_for_all.clicked.connect(
            self.get_back_from_set_optional_alerts_for_reflex_charge)

    def get_back_from_set_charge_current_for_reflex_charge(self):
        self.reflex_charge_values[0] = self.num_pad_.num_pad_input_value.text()
        self.goto_reflex_charge()
        self.set_reflex_charge_values()

    def get_back_from_set_charge_time_for_reflex_charge(self):
        self.reflex_charge_values[1] = self.num_pad_.num_pad_input_value.text()
        self.goto_reflex_charge()
        self.set_reflex_charge_values()

    def get_back_from_set_charge_voltage_for_reflex_charge(self):
        self.reflex_charge_values[2] = self.num_pad_.num_pad_input_value.text()
        self.goto_reflex_charge()
        self.set_reflex_charge_values()

    def get_back_from_set_terminate_when_for_reflex_charge(self):
        self.reflex_charge_values[3] = self.num_pad_.num_pad_input_value.text()
        self.goto_reflex_charge()
        self.set_reflex_charge_values()

    def get_back_from_set_optional_alerts_for_reflex_charge(self):
        self.reflex_charge_values[4] = self.num_pad_.num_pad_input_value.text()
        self.goto_reflex_charge()
        self.set_reflex_charge_values()

    def set_reflex_charge_values(self):
        self.reflex_charge_.set_charge_current_for_reflex_charge.setText(
            self.reflex_charge_values[0])
        self.reflex_charge_.set_charge_time_for_reflex_charge.setText(
            self.reflex_charge_values[1])
        self.reflex_charge_.set_charge_volatge_for_reflex_charge.setText(
            self.reflex_charge_values[2])

        if self.reflex_charge_values[3] == "":
            pass
        else:
            if self.reflex_charge_values[3] == "A":
                self.reflex_charge_.set_reflex_type_A_for_reflex_charge.setChecked(True)
            elif self.reflex_charge_values[3] == "B":
                self.reflex_charge_.set_reflex_type_B_for_reflex_charge.setChecked(True)
            else:
                pass

        self.reflex_charge_.set_optional_alerts_for_reflex_charge.setText(
            self.reflex_charge_values[4])

    def goto_set_charge_current_for_dis_charge(self):
        self.open_num_pad()
        self.buttons_cancel_ok_.btn_ok_for_all.clicked.connect(
            self.get_back_from_set_charge_current_for_dis_charge)

    def goto_set_charge_time_for_dis_charge(self):
        self.open_num_pad()
        self.buttons_cancel_ok_.btn_ok_for_all.clicked.connect(
            self.get_back_from_set_charge_time_for_dis_charge)

    def goto_set_charge_voltage_for_dis_charge(self):
        self.open_num_pad()
        self.buttons_cancel_ok_.btn_ok_for_all.clicked.connect(
            self.get_back_from_set_charge_voltage_for_dis_charge)

    def goto_set_terminate_when_for_dis_charge(self):
        self.open_num_pad()
        self.buttons_cancel_ok_.btn_ok_for_all.clicked.connect(
            self.get_back_from_set_terminate_when_for_dis_charge)

    def goto_set_optional_alerts_for_dis_charge(self):
        self.open_num_pad()
        self.buttons_cancel_ok_.btn_ok_for_all.clicked.connect(
            self.get_back_from_set_optional_alerts_for_dis_charge)

    def get_back_from_set_charge_current_for_dis_charge(self):
        self.dis_charge_values[0] = self.num_pad_.num_pad_input_value.text()
        self.goto_discharge()
        self.set_dis_charge_values()

    def get_back_from_set_charge_time_for_dis_charge(self):
        self.dis_charge_values[1] = self.num_pad_.num_pad_input_value.text()
        self.goto_discharge()
        self.set_dis_charge_values()

    def get_back_from_set_charge_voltage_for_dis_charge(self):
        self.dis_charge_values[2] = self.num_pad_.num_pad_input_value.text()
        self.goto_discharge()
        self.set_dis_charge_values()

    def get_back_from_set_terminate_when_for_dis_charge(self):
        self.dis_charge_values[3] = self.num_pad_.num_pad_input_value.text()
        self.goto_discharge()
        self.set_dis_charge_values()

    def get_back_from_set_optional_alerts_for_dis_charge(self):
        self.dis_charge_values[4] = self.num_pad_.num_pad_input_value.text()
        self.goto_discharge()
        self.set_dis_charge_values()

    def set_dis_charge_values(self):
        self.discharge_.set_dis_charge_current_for_discharge.setText(
            self.dis_charge_values[0])
        self.discharge_.set_dis_charge_time_for_discharge.setText(
            self.dis_charge_values[1])
        self.discharge_.set_dis_charge_volatge_for_discharge.setText(
            self.dis_charge_values[2])
        self.discharge_.set_optional_alerts_for_discharge.setText(
            self.dis_charge_values[4])
