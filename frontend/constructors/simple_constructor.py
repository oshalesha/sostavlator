from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

import frontend.main.my_calendar as clndr
import frontend.main.time_table as tb

from datetime import datetime



class SimpleTaskConstructor:
    _time_minute: TextInput
    _time_hour: TextInput
    _category: Category
    _importance: Importance
    _popup: Popup
    _task_name: str
    _callback: RePlanning
    _status: False
    task = None

    def __init__(self):
        stc = SimpleTaskConstructor

        stc.task = None
        stc._popup = Popup()
        stc._callback = RePlanning()

        stc._task_name = TextInput()
        stc._category = 0
        stc._importance = 0
        stc._time_hour = TextInput()
        stc._time_hour.text = "00"
        stc._time_minute = TextInput()
        stc._time_minute.text = "00"
        stc._status = False

    def window(self):
        stc = SimpleTaskConstructor
        if stc.task is not None:
            stc._task_name.text = stc.task.get_action()
            stc._category = stc.task.get_category()
            stc._importance = stc.task.get_importance().value
            # TODO: there no get time at the moment
            stc._time_hour.text = str(datetime.now().hour)
            stc._time_minute.text = str(datetime.now().minute)
            stc._status = stc.task.get_status()

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
        return RePlanning()

    @staticmethod
    def save(button):
        stc = SimpleTaskConstructor
        if SimpleTaskConstructor._task_name.text == "":
            return
        today = clndr.Calendar.current_date()
        timer = datetime(today.year, today.month, today.day,
                         int(stc._time_hour.text), int(stc._time_minute.text))
        new_task = SimpleTask(action=stc._task_name.text, category=stc._category, scheduled=timer,
                              importance=Importance(stc._importance), status=stc._status)
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
            stc._importance = 0
            button.text = Importance(0).name
        else:
            stc._importance += 1
            button.text = Importance(stc._importance).name

    @staticmethod
    def change_category(button):
        stc = SimpleTaskConstructor
        if stc._category == len(Category) - 1:
            stc._category = 0
            button.text = Category(0).name
        else:
            stc._category += 1
            button.text = Category(stc._category).name
