from Loggers import CheckMarkLogger as NoteTaskLogger, TimeLogger as SimpleTaskLogger, NotesManager
from scheduling.planning import SimpleTask, NoteTask


# TODO: work with simple task


class TasksLoger:

    @staticmethod
    def add_note(note: str):
        NotesManager().add_check_mark_cell(note)

    @staticmethod
    def remove_note(note: str):
        NotesManager().remove_check_mark_cell(note)

    @staticmethod
    def add(task):
        if isinstance(task, NoteTask):
            NoteTaskLogger(task.note).add_check_mark_cell(task)
        else:
            pass

    @staticmethod
    def update(old, new):
        if isinstance(old, NoteTask):
            NoteTaskLogger(old.note).update_check_mark_cell(old, new)
        else:
            pass

    @staticmethod
    def remove(task):
        if isinstance(task, NoteTask):
            NoteTaskLogger(task.note).remove_check_mark_cell(task)
        else:
            pass
