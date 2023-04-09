from CellObjects import CheckMarkCell as NoteTask, TimeCell as SimpleTask


class Note:
    def __init__(self, name, tasks):
        self.name = name
        self.tasks = tasks


class Plan:
    def __init__(self, simple_tasks=None, notes=None):
        if notes is None:
            notes = []
        if simple_tasks is None:
            simple_tasks = []

        self.simple_tasks = simple_tasks
        self.notes = notes
