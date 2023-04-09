from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

from scheduling.planning import NoteTask, SimpleTask, Plan, Note, Category, Importance
import frontend.my_calendar as clndr
import frontend.time_table as tb

from enum import Enum
from abc import ABC, abstractmethod
from datetime import time, datetime


class Constructor(ABC):
    @abstractmethod
    def window(self):
        raise NotImplementedError()

    @abstractmethod
    def callback(self):
        raise NotImplementedError()


#############################################################


class CallBack:
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
        # [note]
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


#############################################################


class SimpleTaskConstructor(Constructor):
    _time_minute: TextInput
    _time_hour: TextInput
    _category: Category
    _importance: Importance
    _popup: Popup
    _task_name: str
    _callback: CallBack
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
            stc._category = stc.task.get_category()
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
        stc = SimpleTaskConstructor
        if SimpleTaskConstructor._task_name.text == "":
            return
        today = clndr.Calendar.current_date()
        timer = datetime(today.year, today.month, today.day,
                         hour=int(stc._time_hour.text), minute=int(stc._time_minute.text))
        new_task = SimpleTask(action=stc._task_name.text, category=stc._category,
                              importance=Importance(stc._importance),
                              date_time=str(timer) + ".0")
        if stc.task is None:
            stc._callback.added_simple_tasks.append(new_task)
        else:
            stc._callback.updated_simple_tasks.append((stc.task, new_task))
        SimpleTaskConstructor._popup.dismiss()
        tb.TimeTable.update_plan(stc._callback)

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
    _popup: Popup
    _note_name: str
    _callback: CallBack

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
        ntc = NoteTaskConstructor
        if ntc._note_name.text == "":
            return
        ntc._callback.added_notes.append(ntc._note_name.text)
        NoteTaskConstructor._popup.dismiss()

    @staticmethod
    def cancel(button):
        NoteTaskConstructor._popup.dismiss()

    def callback(self):
        return CallBack()


#############################################################

