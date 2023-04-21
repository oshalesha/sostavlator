from datetime import date

import scheduling.planning as pl
from Loggers.Loggers import CheckMarkLogger as NoteTaskLogger, TimeLogger as SimpleTaskLogger, NotesManager


class TasksLogger:

    @staticmethod
    def add_note(note: str):
        NotesManager().add(note)

    @staticmethod
    def remove_note(note: str):
        NoteTaskLogger(note).clear()
        NotesManager().remove(note)

    @staticmethod
    def add(task):
        """simple task or note with only one task"""
        if isinstance(task, pl.Note):
            loger = NoteTaskLogger(task.name)
            loger.add(task.tasks[0])
        elif isinstance(task, pl.SimpleTask):
            SimpleTaskLogger().add(task)
        else:
            raise RuntimeError("unknown task in loger add")

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
                loger.rename(old_task.get_action(), new_task.get_action())

        elif isinstance(old, pl.SimpleTask):
            loger = SimpleTaskLogger()
            if old.get_status() != new.get_status():
                loger.set_status(name=old.get_action(), year=old.get_scheduled().year,
                                 month=old.get_scheduled().month, day=old.get_scheduled().day, status=new.get_status())
            elif old.get_action() != new.get_action():
                loger.rename(old_name=old.get_action(), new_name=new.get_action(), year=old.get_scheduled().year,
                             month=old.get_scheduled().month, day=old.get_scheduled().day)
            else:
                # TODO: category and importance and time changes?
                pass
        else:
            raise RuntimeError("unknown task in loger update")

    @staticmethod
    def remove(task):
        """simple task or note with only one task"""
        if isinstance(task, pl.Note):
            loger = NoteTaskLogger(task.name)
            loger.remove(task.tasks[0])
        elif isinstance(task, pl.SimpleTask):
            SimpleTaskLogger().remove(task)
        else:
            raise RuntimeError("unknown task in loger remove")

    @staticmethod
    def pull_out_notes():
        notes = list()
        for _ in NotesManager().get_list():
            pass
            # TODO: pull
            # notes.append(pl.Note(note_name, NoteTaskLogger(note_name).))
        return notes

    @staticmethod
    def pull_out_tasks(day: date):
        return SimpleTaskLogger().get_for_day(day.year, day.month, day.day)
