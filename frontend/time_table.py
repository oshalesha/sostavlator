from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup

import core.manager as mn
import scheduling.planning
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
        TimeTable.constructor = constructors.SimpleTaskConstructor()
        add_window = TimeTable.constructor.window()
        add_window.bind(on_dismiss=TimeTable.add_callback)
        add_window.open()

    @staticmethod
    def add_callback(popup):
        TimeTable.update_plan(TimeTable.constructor.callback())


    @staticmethod
    def open_notes(button):
        NotesWindow().open()


#########################################################################


class TaskButton(GridLayout):
    def __init__(self, task: SimpleTask, **kwargs):
        super().__init__(**kwargs)
        self.task = task
        self.cols = 2

        done_button = Button()
        done_button.text = "undone" if task.get_status() else "done"
        done_button.bind(on_press=self.done)
        self.done_button = done_button
        self.add_widget(done_button)

        task_button = Button()
        task_button.text = task.get_action()
        task_button.bind(on_release=self.task_config)
        self.task_button = task_button
        self.add_widget(task_button)

    def done(self, button):
        callback = scheduling.planning.RePlanning()
        new_version = self.task
        new_version.set_status(not new_version.get_status())
        callback.updated_simple_tasks.append((self.task, new_version))
        TimeTable.update_plan(callback)

    def task_config(self, button):
        self.cns = constructors.SimpleTaskConstructor()
        constructors.SimpleTaskConstructor.task = self.task
        window = self.cns.window()
        window.bind(on_dismiss=self.callback)
        window.open()

    def callback(self, instance):
        TimeTable.update_plan(self.cns.callback())

#########################################################################


class NotesWindow(Popup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.content = GridLayout()
        self.content.cols = 3
        self.content.rows = 2
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
        self.cns = constructors.NoteConstructor()
        add_window = self.cns.window()
        add_window.bind(on_dismiss=self.callback)
        add_window.open()

    def callback(self, popup):
        TimeTable.update_plan(self.cns.callback())
        self.redraw()

    def redraw(self):
        self.content.clear_widgets()
        notes = TimeTable.plan.notes
        for note in notes:
            self.content.add_widget(self.real_note_button(note))

        if len(notes) < self.content.cols * self.content.rows:
            btn = Button()
            btn.text = "add"
            btn.bind(on_release=self.add_note)
            self.content.add_widget(btn)
        for i in range(self.content.cols * self.content.rows - 2 - len(notes)):
            self.content.add_widget(empty_space())
        self.content.add_widget(Button(text="close", on_release=self.close))

    def close(self, instance):
        self.dismiss()


#########################################################################


def empty_space():
    btn = Button()
    btn.background_color = [0, 0, 0, 0]
    return btn
