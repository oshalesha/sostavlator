from CellObjects.CellObjects import CheckMarkCell as NoteTask
from CellObjects.CellObjects import TimeCell as SimpleTask
from CellObjects.CellObjects import Category
from CellObjects.CellObjects import Importance


class Note:
    def __init__(self, name: str, tasks: list[NoteTask]):
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


###################################################################################


class RePlanning:
    def __init__(self):
        # [SimpleTask]
        self.added_simple_tasks = list()
        # [(SimpleTask, SimpleTask)]
        self.updated_simple_tasks = list()
        # [SimpleTask]
        self.removed_simple_tasks = list()
        # [str]
        self.added_notes = list()
        # [(note, note)]
        self.updated_notes = list()
        # [str]
        self.removed_notes = list()

    # TODO: shape for only notes
    def shape(self, plan: Plan):
        for task in self.added_simple_tasks:
            plan.simple_tasks.append(task)

        for pair in self.updated_simple_tasks:
            for index, value in enumerate(plan.simple_tasks):
                if pair[0] == value:
                    plan.simple_tasks[index] = pair[1]

        for task in self.removed_simple_tasks:
            if task in plan.simple_tasks:
                plan.simple_tasks.remove(task)

        plan.notes = self.shape_notes(plan.notes)
        return plan

    def shape_notes(self, notes):
        for name in self.added_notes:
            notes.append(Note(name=name, tasks=list()))

        for pair in self.updated_notes:
            for index, value in enumerate(notes):
                if pair[0].name == value.name:
                    notes[index] = pair[1]

        for note in self.removed_notes:
            for index, value in enumerate(notes):
                if note.name == value.name:
                    notes.remove(value)
        return notes
