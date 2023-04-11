from Loggers import CheckMarkLogger as NoteTaskLogger, TimeLogger as SimpleTaskLogger, NotesManager
import scheduling.planning as pl


class TasksLoger:

    @staticmethod
    def add_note(note: str):
        NotesManager().add(note)

    @staticmethod
    def remove_note(note: str):
        NotesManager().remove(note)

    @staticmethod
    def add(task):
        """simple task or note with only one task"""
        if isinstance(task, pl.Note):
            loger = NoteTaskLogger(task.name)
            loger.add_check_mark_cell(task.tasks[0])
        elif isinstance(task, pl.SimpleTask):
            SimpleTaskLogger().add_time_cell(task)
        else:
            raise TypeError("unknown task in loger add")

    @staticmethod
    def update(old, new):
        """simple task or note with only one task"""

        if isinstance(old, pl.Note):
            old_task = old.tasks[0]
            new_task = new.tasks[0]
            loger = NoteTaskLogger(old.name)

            if old_task.get_status() != new_task.get_status():
                loger.set_status(old_task.get_action(), new_task.get_status())
            elif old_task.get_action() != old_task.get_action():
                loger.rename_check_mark_cell(old_task.get_action(), new_task.get_action())

        elif isinstance(old, pl.SimpleTask):
            SimpleTaskLogger().update_time_cell(old, new)
        else:
            raise TypeError("unknown task in loger update")

    @staticmethod
    def remove(task):
        """simple task or note with only one task"""
        if isinstance(task, pl.Note):
            loger = NoteTaskLogger(task.name)
            loger.remove_check_mark_cell(task.tasks[0])
        elif isinstance(task, pl.SimpleTask):
            SimpleTaskLogger().remove_time_cell(task)
        else:
            raise TypeError("unknown task in loger remove")

    @staticmethod
    def pull_out_notes():
        pass
