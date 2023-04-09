from frontend.time_table import TimeTable
from scheduling.scheduler import Scheduler


class Manager:
    @staticmethod
    def set_date(day):
        plan = Scheduler.get_plan(day)
        TimeTable.show(plan)

    @staticmethod
    def update(callback):
        pass
