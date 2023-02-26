from UI_imports import Ui_number_pad_form, Ui_cancel_ok_buttons_form
from requirements import LABELS_OF_BUTTONS
import functools


class NumPad(object):
    def __init__(self, workspace, buttons_space):
        self.workspace = workspace
        self.buttons_space = buttons_space

        self.num_pad = Ui_number_pad_form()
        self.buttons_cancel_ok = Ui_cancel_ok_buttons_form()

    def set_up_ui(self):
        self.num_pad.setupUi(self.workspace)
        self.num_pad.win_number_pad.show()

        self.buttons_cancel_ok.setupUi(self.buttons_space)
        self.buttons_cancel_ok.cancel_ok_buttons_win.show()

        self.set_num_pad_buttons()

    def set_num_pad_buttons(self):
        btn_num_pad = [self.num_pad.btn_1_num_pad, self.num_pad.btn_2_num_pad, self.num_pad.btn_3_num_pad,
                       self.num_pad.btn_4_num_pad, self.num_pad.btn_5_num_pad, self.num_pad.btn_6_num_pad,
                       self.num_pad.btn_7_num_pad, self.num_pad.btn_8_num_pad, self.num_pad.btn_9_num_pad,
                       self.num_pad.btn_semi_colon_num_pad, self.num_pad.btn_0_num_pad,
                       self.num_pad.btn_dot_num_pad, ]

        self.num_pad.delete_input_value.clicked.connect(self.num_pad_backspace)

        for index, btn in enumerate(btn_num_pad):
            btn.clicked.connect(
                functools.partial(self.set_value, "{}".format(LABELS_OF_BUTTONS[index])))

    def get_value(self):
        return self.num_pad.num_pad_input_value.text()

    def set_value(self, value):
        old_value = self.num_pad.num_pad_input_value.text()
        new_value = old_value + value

        self.num_pad.num_pad_input_value.setText(new_value)

    def num_pad_backspace(self):
        text = self.num_pad.num_pad_input_value.text()
        if len(text) == 0:
            pass
        else:
            new_text = text[:-1]
            self.num_pad.num_pad_input_value.setText(new_text)
