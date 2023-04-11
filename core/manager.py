import frontend.time_table as tb

from scheduling.scheduler import Scheduler


class Manager:
    @staticmethod
    def set_date(day):
        plan = Scheduler.get_plan(day)
        tb.TimeTable.show(plan)

    @staticmethod
    def update(callback):
        Scheduler.update(callback)
