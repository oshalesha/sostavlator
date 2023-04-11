from datetime import date

from scheduling.planning import Plan, SimpleTask, NoteTask


class Scheduler:

    @staticmethod
    def get_plan(day: date):
        return Plan()

    @staticmethod
    def update(callback):
        pass


