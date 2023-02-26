import asyncio
import datetime
import time
from PyQt5.QtCore import QTimer, QThreadPool
from UI_imports import Ui_charging_status_form, Ui_stop_next_pause_buttons_form
from background_workers import Worker
from rpi_arduino_i2c_comm import write_data_to_arduino, read_data_from_arduino
from table_view_data_model import TableModel


class ChargingScreen(object):
    def __init__(self, workspace, buttons_space, charge_config, mode):
        self.workspace = workspace
        self.buttons_space = buttons_space
        self.charge_config = charge_config
        self.mode = mode

        self.timer = QTimer()
        self.threadpool = QThreadPool()

        self.charging_status = Ui_charging_status_form()
        self.buttons_stop_next_pause = Ui_stop_next_pause_buttons_form()

        self.running = True

    def set_up_ui(self):
        self.charging_status.setupUi(self.workspace)
        self.charging_status.win_charging_status.show()

        self.buttons_stop_next_pause.setupUi(self.buttons_space)
        self.buttons_stop_next_pause.stop_next_pause_buttons_win.show()

        self.set_button_calls()

    def set_button_calls(self):
        return

    def start_charging_process(self):
        try:
            self.charging_status.charge_current_display.display(self.charge_config[0])
            self.charging_status.remaining_time.setText(self.charge_config[1])
            self.charging_status.charge_voltage_display.display(self.charge_config[2])
            self.charging_status.view_charge_type.setText(self.mode)

            table_model = TableModel(data=[self.charge_config])
            self.charging_status.show_charge_info.setModel(table_model)

            self.start_i2c_comm_worker()
            self.start_count_down_timer_worker()
        except Exception as e:
            print(e)

    def start_count_down_timer_worker(self):
        timer_worker = Worker(self.start_count_down_timer)
        self.threadpool.start(timer_worker)

    def start_count_down_timer(self):
        date = datetime.date.today()
        hour, minute, second = str(self.charge_config[1]).split(':')
        hour, minute, second = int(hour), int(minute), int(second)
        year, month, day = date.year, date.month, date.day

        date_time_ = datetime.datetime(year=year, month=month, day=day, hour=hour, minute=minute, second=second)
        date_time_delta = datetime.timedelta(seconds=1)

        while self.running:
            date_, time_ = str(date_time_).split(' ')
            self.charging_status.remaining_time.setText(time_)
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
