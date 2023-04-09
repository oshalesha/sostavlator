from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

from scheduling.planning import NoteTask, SimpleTask, Plan, Note, Category, Importance

from enum import Enum
from abc import ABC, abstractmethod
from datetime import time


class Constructor(ABC):
    @abstractmethod
    def window(self):
        raise NotImplementedError()

    @abstractmethod
    def callback(self):
        raise NotImplementedError()

#############################################################


class SimpleTaskConstructor(Constructor):
    _time_minute = None
    _time_hour = None
    _category = None
    _importance = None
    _popup = None
    _task_name = None
    task = None

    def __init__(self):
        stc = SimpleTaskConstructor

        stc.task = None
        stc._popup = Popup()
        stc._callback = CallBack()

        stc._task_name = TextInput()
        stc._category = 0
        stc._importance = 0
        stc._time_hour = TextInput()
        stc._time_hour.text = "00"
        stc._time_minute = TextInput()
        stc._time_minute.text = "00"

    def window(self):
        stc = SimpleTaskConstructor
        if stc.task is not None:
            stc._task_name.text = stc.task.get_action()
            stc._category = stc.task.get_category().value
            stc._importance = stc.task.get_importance().value
            stc._time_hour.text = str(stc.task.get_date_time().hour)
            stc._time_minute.text = str(stc.task.get_date_time().minute)

        window = GridLayout()
        window.rows = 3
        window.cols = 2

        timer = GridLayout()
        timer.cols = 2
        timer.add_widget(stc._time_hour)
        timer.add_widget(stc._time_minute)

        window.add_widget(stc._task_name)
        window.add_widget(timer)
        window.add_widget(Button(text=Importance(stc._importance).name,
                                 on_release=stc.change_importance))
        window.add_widget(Button(text=Category(stc._category).name,
                                 on_release=stc.change_category))
        window.add_widget(Button(text="save", on_release=stc.save))
        window.add_widget(Button(text="cancel", on_release=stc.cancel))

        # TODO: hints
        stc._popup.content = window
        return stc._popup

    def callback(self):
        return CallBack()

    @staticmethod
    def save(button):
        if SimpleTaskConstructor._task_name.text == "":
            return
        # TODO: work with callback
        SimpleTaskConstructor._popup.dismiss()

    @staticmethod
    def cancel(button):
        SimpleTaskConstructor._popup.dismiss()

    @staticmethod
    def change_importance(button):
        stc = SimpleTaskConstructor
        if stc._importance == len(Importance) - 1:
            button.text = Importance(0).name
        else:
            stc._importance += 1
            button.text = Importance(stc._importance).name

    @staticmethod
    def change_category(button):
        stc = SimpleTaskConstructor
        if stc._category == len(Category) - 1:
            button.text = Category(0).name
        else:
            stc._category += 1
            button.text = Category(stc._category).name

#############################################################


class NoteTaskEditor(Constructor):
    # note is set by user class

    def window(self):
        return Popup()

    def callback(self):
        return CallBack()


#############################################################


class NoteTaskConstructor(Constructor):
    _popup = None
    _note_name = None
    _callback = None

    def __init__(self):
        ntc = NoteTaskConstructor
        ntc._popup = Popup()
        ntc._note_name = TextInput()
        ntc._callback = CallBack()

    def window(self):
        # can't save it as object fields due to kivy popup behavior
        ntc = NoteTaskConstructor

        window = GridLayout()
        window.rows = 4

        window.add_widget(Label(text="enter the name"))
        window.add_widget(ntc._note_name)
        window.add_widget(Button(text="save", on_release=ntc.save_name))
        window.add_widget(Button(text="cancel", on_release=ntc.cancel))

        ntc._popup.content = window
        return ntc._popup

    @staticmethod
    def save_name(button):
        if NoteTaskConstructor._note_name.text == "":
            return
        # TODO: work with callback
        NoteTaskConstructor._popup.dismiss()

    @staticmethod
    def cancel(button):
        NoteTaskConstructor._popup.dismiss()

    def callback(self):
        return CallBack()


#############################################################


class CallBack:
    class TYPE(Enum):
        Note = 0,
        NoteTask = 1,
        SimpleTask = 2

    class CHANGE(Enum):
        Add = 0,
        Update = 1,
        Remove = 2

    def shape(self, plan: Plan):
        return plan