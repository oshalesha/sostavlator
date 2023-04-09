from CellObjects import CheckMarkCell, TimeCell as SimpleTask


class NoteTask(CheckMarkCell):
    def __init__(self, note, **kwargs):
        super().__init__(**kwargs)
        self.note = note


class Plan:
    def __init__(self, simple_tasks=None, notes=None):
        if notes is None:
            notes = []
        if simple_tasks is None:
            simple_tasks = []
        self.simple_tasks = simple_tasks
        self.notes = notes
