from CellObjects import CheckMarkCell, TimeCell as SimpleTask


class NoteTask(CheckMarkCell):
    def __init__(self, note, **kwargs):
        super().__init__(**kwargs)
        self.note = note


class Plan:
    pass