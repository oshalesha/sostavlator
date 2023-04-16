from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

from calendar import monthrange, month_name
from datetime import date

from frontend.design.support import empty_space


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


class Calendar(GridLayout):

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
        left = Button()
        left.text = "left"
        left.bind(on_press=self.left_move)

        right = Button()
        right.text = "right"
        right.bind(on_press=self.right_move)

        # label
        self.label = Label()
        self.update_label()

        # buttons line
        top = GridLayout()
        top.cols = 3
        top.add_widget(left)
        top.add_widget(self.label)
        top.add_widget(right)
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
                self.add_widget(empty_space())
            for i in range(month_info[1]):
                self.add_widget(self.day_button(i + 1))

        def day_button(self, day):
            button = Button()
            button.text = str(day)
            button.bind(on_press=self.day_reset)
            return button

        def day_reset(self, button):
            self.window._set_date(date(self.window.month['year'],
                                       self.window.month['month'],
                                       int(button.text)))
