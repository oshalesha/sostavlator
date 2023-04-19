from kivy.uix.gridlayout import GridLayout

import core.today as today
import frontend.main.my_calendar as cld
import frontend.main.time_table as tb
import scheduling.scheduler as scheduler


class Manager(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__scheduler = scheduler.Scheduler()
        self.__table = tb.TimeTable(callback=self.change_in_plan)
        self.__calendar = cld.Calendar(set_date_callback=self.set_date)

        self.cols = 2
        self.add_widget(self.__table)
        self.add_widget(self.__calendar)

    def set_date(self, day):
        plan = self.__scheduler.get_plan(day)
        today.set_date(day)
        self.__table.show(plan)

    def change_in_plan(self, callback):
        self.__scheduler.update(callback)
