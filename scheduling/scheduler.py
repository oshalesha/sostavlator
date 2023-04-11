from datetime import date

import scheduling.planning as pl
import scheduling.tasks_loger as tl


class Scheduler:

    @staticmethod
    def get_plan(day: date):
        return pl.Plan(tl.TasksLoger.pull_out_tasks(day),
                       tl.TasksLoger.pull_out_notes())

    @staticmethod
    def update(re_plan: pl.RePlanning):
        logger = tl.TasksLoger
        for task in re_plan.added_simple_tasks:
            logger.add(task)
        for pair in re_plan.updated_simple_tasks:
            logger.update(pair[0], pair[1])
        for task in re_plan.removed_simple_tasks:
            logger.remove(task)

        for note in re_plan.added_notes:
            logger.add_note(note)
        for pair in re_plan.updated_notes:
            logger.update(pair[0], pair[1])
        for note in re_plan.removed_notes:
            logger.remove_note(note)


