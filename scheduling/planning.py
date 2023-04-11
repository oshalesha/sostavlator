from CellObjects import CheckMarkCell as NoteTask, TimeCell as SimpleTask, Category, Importance


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

        for name in self.added_notes:
            plan.notes.append(Note(name=name, tasks=list()))

        for pair in self.updated_notes:
            for index, value in enumerate(plan.notes):
                if pair[0].name == value.name:
                    plan.simple_tasks[index] = pair[1]

        for note in self.removed_notes:
            for index, value in enumerate(plan.notes):
                if note.name == plan.notes:
                    plan.notes.remove(value)
        return plan
