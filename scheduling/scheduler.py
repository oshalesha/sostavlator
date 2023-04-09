from datetime import date

from scheduling.planning import Plan, SimpleTask, NoteTask
from scheduling.tasks_loger import TasksLoger


class Scheduler:

    @staticmethod
    def get_plan(day: date):
        return Plan()

    @staticmethod
    def update(callback):
        pass


