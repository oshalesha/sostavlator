from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label

import frontend.constructors.note_constructors as note_cns
import frontend.constructors.simple_constructors as simple_cns
import frontend.design.colors as colors
import frontend.design.support as support
import scheduling.planning as pl


class AddSimpleTaskButton(ButtonBehavior, Image):
    def __init__(self, callback, **kwargs):
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

        self.cols = 3

        # done button
        done_button = support.ButtonImage()
        done_button.source = support.simple_task_status_image(task)
        done_button.size_hint = (0.25, 1)
        done_button.bind(on_press=self.done)
        self.done_button = done_button
        self.add_widget(done_button)

        # task button
        task_button = support.ButtonText()
        task_button.text = task.get_action()
        task_button.color = colors.task_category_color(self.__task.get_category().value, theme="white")
        task_button.font_size = 28
        task_button.bind(on_release=self.task_config)
        self.task_button = task_button
        self.add_widget(task_button)

        # time label
        time = Label()
        minute = str(task.get_scheduled().minute)
        time.text = (str(task.get_scheduled().hour) + ':' + (minute if len(minute) == 2 else '0' + minute))
        time.size_hint = (0.3, 1)
        time.color = [0, 0, 0, 1]
        time.font_size = 24
        self.add_widget(time)

    def done(self, button):
        callback = pl.RePlanning()
        new_version = self.__task.copy()
        new_version.set_status(not new_version.get_status())
        callback.updated_simple_tasks.append((self.__task, new_version))
        self._callback(callback, redraw=False)
        self.__task.set_status(new_version.get_status())
        self.done_button.source = support.simple_task_status_image(self.__task)

    def task_config(self, button):
        simple_cns.SimpleTaskRedactor(callback=self.callback, task=self.__task).open()

    def callback(self, callback, redraw=True):
        self._callback(callback, redraw)


#####################################################################


class AddNoteButton(support.ButtonImage):
    def __init__(self, callback, **kwargs):
        super().__init__(**kwargs)
        self.__callback = callback

    def on_press(self):
        note_cns.NoteConstructor(callback=self.__callback).open()


#####################################################################


class NoteTaskButton(support.ImageLayout):
    def __init__(self, note: pl.Note, task: pl.NoteTask, callback, **kwargs):
        super().__init__(**kwargs)
        self.__task = task
        self.__callback = callback
        self.__note = note
        self.cols = 2

        done_btn = support.ButtonImage()
        done_btn.on_press = self.done
        done_btn.source = support.note_tasks_status_image(self.__task)
        self.add_widget(done_btn)

        note_redact_btn = support.ButtonText()
        note_redact_btn.on_press = self.config
        note_redact_btn.text = task.get_action()

    def update(self, callback):
        pass

    def done(self):
        pass

    def config(self):
        pass


#####################################################################


class AddNoteTaskButton(support.ButtonImage):
    def __init__(self, note, callback, **kwargs):
        super().__init__(**kwargs)
        self.__callback = callback
        # TODO: bind with open constructor


#####################################################################


class NoteLabel(support.ButtonText):
    def __init__(self, name, callback, **kwargs):
        super().__init__(**kwargs)
        self.text = name
        self.__callback = callback
        # TODO: bind with open redactor

#####################################################################


def note_predictions(tasks_window) -> list:
    pass

