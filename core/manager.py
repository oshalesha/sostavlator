import frontend.time_table as tb

if __name__ == "__main__":
    from scheduling.scheduler import Scheduler


class Manager:
    @staticmethod
    def set_date(day):
        plan = Scheduler.get_plan(day)
        tb.TimeTable.show(plan)

    @staticmethod
    def update(callback):
        pass
