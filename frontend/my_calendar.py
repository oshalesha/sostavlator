import calendar

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout

import calendar
from datetime import date


class Calendar(FloatLayout):
    date = date.today()

    def draw_month(self, year, month):
        days = calendar.monthrange(year, month)


    def __init__(self, **kwargs):
        super(Calendar, self).__init__(**kwargs)

        # add left button
