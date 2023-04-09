from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button

from scheduling.planning import Plan, SimpleTask, NoteTask


class TimeTable:
    plan = Plan()
    tasks_counter = 12
    table: GridLayout

    @staticmethod
    def show(plan: Plan):
        TimeTable.plan = plan
        TimeTable.redraw_tasks()

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
            TimeTable.table.add_widget(TimeTable.TaskButton(task))

        # empty spaces
        for i in range(TimeTable.tasks_counter - len(TimeTable.plan.simple_tasks)):
            TimeTable.table.add_widget(TimeTable.empty_space())

        # Notes button
        note_btn = Button()
        note_btn.text = "open notes"
        note_btn.bind(on_press=TimeTable.open_notes)

        TimeTable.table.add_widget(note_btn)

    @staticmethod
    def add_press(button):
        pass

    @staticmethod
    def open_notes(button):
        pass

    @staticmethod
    def empty_space():
        btn = Button()
        btn.background_color = [0, 0, 0, 0]
        return btn

    # TODO: add buttons actions
    class TaskButton(GridLayout):
        def __init__(self, task: SimpleTask, **kwargs):
            super().__init__(**kwargs)
            self.task = task

            done_button = Button()
            done_button.text("done")
            self.add_widget(done_button)

            task_button = Button()
            task_button.text(task.get_action())
            self.add_widget(task_button)

