from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout

from frontend.constructors.simple_constructor import SimpleTaskConstructor
from scheduling import planning as pl


class AddTaskButton(Button):
    def __init__(self, callback, **kwargs):
        super().__init__(**kwargs)
        self._callback = callback
        # TODO: on_push


class SimpleTaskButton(GridLayout):
    def __init__(self, task: pl.SimpleTask, callback, **kwargs):
        super().__init__(**kwargs)
        self._callback = callback
        self.__task = task

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
        callback = pl.RePlanning()
        new_version = self.__task
        new_version.set_status(not new_version.get_status())
        callback.updated_simple_tasks.append((self.__task, new_version))
        self._callback(callback, redraw=False)

    def task_config(self, button):
        SimpleTaskConstructor(callback=self.callback).open()

    def callback(self, instance, callback, redraw=True):
        self._callback(callback, redraw)
