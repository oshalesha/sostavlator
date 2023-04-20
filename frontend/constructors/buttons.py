from kivy.uix.button import Button
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image

import frontend.constructors.note_constructors as note_cns
import frontend.constructors.simple_constructors as simple_cns
import frontend.design.colors as colors
import frontend.design.support as support
from scheduling import planning as pl


class AddSimpleTaskButton(ButtonBehavior, Image):
    def __init__(self, callback, *args, **kwargs):
        super().__init__(**kwargs)
        self._callback = callback
        self.source = support.plus_image()

    def on_press(self):
        simple_cns.SimpleTaskConstructor(self._callback).open()


#####################################################################


class SimpleTaskButton(GridLayout):
    def __init__(self, task: pl.SimpleTask, callback, **kwargs):
        super().__init__(**kwargs)
        self._callback = callback
        self.__task = task

        self.cols = 2

        done_button = support.ButtonImage()
        done_button.source = support.task_status_image(task)
        done_button.size_hint = (0.25, 1)
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
        self.__task.set_status(new_version.get_status())
        self.done_button.source = support.task_status_image(self.__task)

    def task_config(self, button):
        simple_cns.SimpleTaskRedactor(callback=self.callback, task=self.__task).open()

    def callback(self, callback, redraw=True):
        self._callback(callback, redraw)


#####################################################################


class AddNoteButton(Button):
    def __init__(self, callback, **kwargs):
        super().__init__(**kwargs)
        self.__callback = callback

    def on_press(self):
        note_cns.NoteConstructor(callback=self.__callback).open()


#####################################################################


class AddNoteTaskButton:
    pass


#####################################################################


class NotetaskButton:
    pass
