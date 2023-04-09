from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup

import core.manager as mn
from scheduling.planning import Plan, SimpleTask
import frontend.constructors as constructors


class TimeTable:
    plan = Plan()
    tasks_counter = 9
    table: GridLayout

    @staticmethod
    def show(plan: Plan):
        TimeTable.plan = plan
        TimeTable.redraw_tasks()

    @staticmethod
    def update_plan(callback):
        TimeTable.plan = callback.shape(TimeTable.plan)
        TimeTable.redraw_tasks()
        mn.Manager.update(callback)

    @staticmethod
    def window():
        table = GridLayout()
        TimeTable.table = table
        GridLayout.rows = TimeTable.tasks_counter + 2

        TimeTable.redraw_tasks()
        return table

    @staticmethod
    def redraw_tasks():
        TimeTable.table.clear_widgets()
        # add button
        add_btn = Button()
        add_btn.text = "add"
        add_btn.bind(on_press=TimeTable.add_press)
        TimeTable.table.add_widget(add_btn)

        # real tasks
        for task in TimeTable.plan.simple_tasks:
            TimeTable.table.add_widget(TaskButton(task))

        # empty spaces
        for i in range(TimeTable.tasks_counter - len(TimeTable.plan.simple_tasks)):
            TimeTable.table.add_widget(empty_space())

        # Notes button
        note_btn = Button()
        note_btn.text = "open notes"
        note_btn.bind(on_press=TimeTable.open_notes)

        TimeTable.table.add_widget(note_btn)

    @staticmethod
    def add_press(button):
        constructor = constructors.SimpleTaskConstructor()
        constructor.window().open()

    @staticmethod
    def open_notes(button):
        popup = Popup(content=NotesWindow())
        popup.open()


#########################################################################


class TaskButton(GridLayout):
    def __init__(self, task: SimpleTask, **kwargs):
        super().__init__(**kwargs)
        self.task = task
        self.cols = 2

        done_button = Button()
        done_button.text = "done"
        done_button.bind(on_press=self.done)
        self.done_button = done_button
        self.add_widget(done_button)

        task_button = Button()
        task_button.text = task.get_action()
        task_button.bind(on_release=self.task_config)
        self.task_button = task_button
        self.add_widget(task_button)

    def done(self, button):
        button.text = "undone"
        callback = constructors.CallBack()
        new_version = self.task
        new_version.set_status(True)
        callback.updated_simple_tasks.append((self.task, new_version))
        TimeTable.update_plan(callback)

    def task_config(self, button):
        cns = constructors.SimpleTaskConstructor()
        constructors.SimpleTaskConstructor.task = self.task
        cns.window().open()


#########################################################################


class NotesWindow(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.notes = TimeTable.plan.notes
        self.cols = 3
        self.rows = 2
        self.redraw()

    @staticmethod
    def real_note_button(note):
        btn = Button()
        btn.text = note.name
        btn.note = note
        btn.bind(on_release=NotesWindow.open_note)
        return btn

    @staticmethod
    def open_note(button):
        cns = constructors.NoteTaskEditor()
        cns.window().open()
        TimeTable.update_plan(cns.callback())

    def add_note(self, button):
        cns = constructors.NoteTaskConstructor()
        cns.window().open()
        TimeTable.update_plan(cns.callback())
        self.notes = TimeTable.plan.notes
        self.redraw()

    def redraw(self):
        self.clear_widgets()
        for note in self.notes:
            self.add_widget(self.real_note_button(note))

        if len(self.notes) < self.cols * self.rows:
            btn = Button()
            btn.text = "add"
            btn.bind(on_release=self.add_note)
            self.add_widget(btn)
        for i in range(self.cols * self.rows - 1):
            self.add_widget(empty_space())


#########################################################################


def empty_space():
    btn = Button()
    btn.background_color = [0, 0, 0, 0]
    return btn
