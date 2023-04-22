from calendar import monthrange, month_name
from datetime import date

from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image

import frontend.design.support as support


################################################################################


def next_month(month: dict):
    if month['month'] == 12:
        month['month'] = 1
        month['year'] += 1
    else:
        month['month'] += 1
    return month


def prev_month(month: dict):
    if month['month'] == 1:
        month['month'] = 12
        month['year'] -= 1
    else:
        month['month'] -= 1
    return month


################################################################################


class Calendar(GridLayout, Image):

    def current_date(self):
        return self.__current__date

    def _set_date(self, new_date):
        self.__current__date = new_date
        self._callback(new_date)

    def __init__(self, set_date_callback, **kwargs):
        super().__init__(**kwargs)
        self._callback = set_date_callback
        self._set_date(date.today())

        self.month = {"year": date.today().year, "month": date.today().month}
        self.rows = 2

        # buttons
        class MoveButton(ButtonBehavior, Image):
            pass

        left = MoveButton()
        left.source = 'frontend/design/pictures/left.png'
        left.size_hint = (0.3, 1)
        left.bind(on_press=self.left_move)

        right = MoveButton()
        right.source = 'frontend/design/pictures/right.png'
        right.size_hint = (0.3, 1)
        right.bind(on_press=self.right_move)

        # label
        self.label = Label(color=(1, 0.35, 0, 1), font_size=24)
        self.update_label()

        # buttons line
        top = GridLayout()
        top.cols = 3
        top.add_widget(left)
        top.add_widget(self.label)
        top.add_widget(right)
        top.size_hint = (1, 0.3)
        self.add_widget(top)

        self.days_table = self.create_days_table()
        self.add_widget(self.days_table)

    def left_move(self, button):
        self.month = prev_month(self.month)
        self.update_label()
        self.redraw_days_table()

    def right_move(self, button):
        self.month = next_month(self.month)
        self.update_label()
        self.redraw_days_table()

    def update_label(self):
        self.label.text = month_name[self.month['month']] + ' ' + str(self.month['year'])

    def create_days_table(self):
        return self.DaysTable(self)

    def redraw_days_table(self):
        self.remove_widget(self.days_table)
        self.days_table = self.create_days_table()
        self.add_widget(self.days_table)

    ############################################################################

    class DaysTable(GridLayout):
        def __init__(self, window, **kwargs):
            super().__init__(**kwargs)
            self.window = window
            self.cols = 7

            # first-day-week, days-in-month
            month_info = monthrange(window.month['year'], window.month['month'])

            for i in range(month_info[0]):
                self.add_widget(support.empty_space())

            self.current_date_button = None
            for i in range(month_info[1]):
                day_btn = self.day_button(i + 1)
                if window.current_date().day == i + 1 and \
                        window.month['year'] == window.current_date().year and \
                        window.month['month'] == window.current_date().month:
                    self.current_date_button = day_btn
                    day_btn.color = (0, 0, 1, 1)
                self.add_widget(day_btn)

        def day_button(self, day):
            button = support.ButtonText()
            button.color = (1, 0.35, 0, 1)
            button.font_size = 28

            button.text = str(day)
            button.bind(on_press=self.day_reset)
            return button

        def day_reset(self, button):
            if self.current_date_button is not None:
                self.current_date_button.color = (1, 0.35, 0, 1)
            self.current_date_button = button
            button.color = (0, 0, 1, 1)
            self.window._set_date(date(self.window.month['year'],
                                       self.window.month['month'],
                                       int(button.text)))
