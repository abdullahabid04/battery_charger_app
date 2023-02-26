from app_gui.home_page import HomePage


class App(object):
    def __init__(self, window):
        self.win = window
        self.home_page = HomePage(self.win)

    def run(self):
        self.home_page.set_up_ui()
        self.win.show()
