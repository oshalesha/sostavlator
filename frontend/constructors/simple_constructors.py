from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

import scheduling.planning as pl
import core.today as td

from datetime import datetime


def importance_name(importance):
    return pl.Importance(importance).name


def category_name(category):
    return pl.Category(category).name


def importance_index(importance):
    for i in pl.Importance:
        if i == importance:
            return i.value


def category_index(category):
    for i in pl.Category:
        if i == category:
            return i.value


#########################################################


# similar part for constructor and redactor
class SimpleTaskCntWindow(Popup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.content = GridLayout()
        self.content.rows = 3

        # create main part
        self._task_name = TextInput()
        self._category = 0
        self._importance = 0
        self._time_minute = TextInput()
        self._time_minute.text = "00"
        self._time_hours = TextInput()
        self._time_hours.text = "00"

        # push everything in content
        self.content.add_widget(self._task_name)

        configs = GridLayout()
        configs.cols = 2
        self._importance_btn = Button(text=importance_name(self._importance), on_release=self.change_importance)
        self._category_btn = Button(text=category_name(self._category), on_release=self.change_category)
        configs.add_widget(self._category_btn)
        configs.add_widget(self._importance_btn)
        self.content.add_widget(configs)

        time = GridLayout()
        time.cols = 2
        time.add_widget(self._time_hours)
        time.add_widget(self._time_minute)
        self.content.add_widget(time)

    def create_task(self):
        today = td.today()
        timer = datetime(today.year, today.month, today.day,
                         int(self._time_hours.text), int(self._time_minute.text))
        return pl.SimpleTask(action=self._task_name.text, category=pl.Category(self._category),
                             scheduled=timer,
                             importance=pl.Importance(self._importance), status=False)

    def change_importance(self, button):
        if self._importance == len(pl.Importance) - 1:
            self._importance = 0
        else:
            self._importance += 1
        self.update_importance()

    def update_importance(self):
        self._importance_btn.text = importance_name(self._importance)

    def change_category(self, button):
        if self._category == len(pl.Category) - 1:
            self._category = 0
        else:
            self._category += 1
        self.update_category()

    def update_category(self):
        self._category_btn.text = category_name(self._category)

    def cancel(self, instance):
        self.dismiss()


#########################################################


class SimpleTaskConstructor(SimpleTaskCntWindow):
    def __init__(self, callback, **kwargs):
        super().__init__(**kwargs)
        self.__callback = callback
        # add manage menu
        self.content.rows += 1
        manage = GridLayout()
        manage.cols = 2

        manage.add_widget(Button(text='save', on_release=self.on_save))
        manage.add_widget(Button(text='cancel', on_release=self.cancel))
        self.content.add_widget(manage)
        # TODO: window with hints

    def on_save(self, instance):
        callback = pl.RePlanning()
        callback.added_simple_tasks.append(self.create_task())
        self.__callback(callback, redraw=True)
        self.dismiss()


##########################################################################


class SimpleTaskRedactor(SimpleTaskCntWindow):
    def __init__(self, callback, task: pl.SimpleTask, **kwargs):
        super().__init__(**kwargs)
        self.__task = task
        self.__callback = callback

        # change fields to current task
        self._task_name.text = task.get_action()
        self._category = category_index(task.get_category())
        self._importance = importance_index(task.get_importance())
        self._time_minute.text = str(task.get_scheduled().minute)
        self._time_hours.text = str(task.get_scheduled().hour)
        self.update_category()
        self.update_importance()

        # add manage menu
        self.content.rows += 1
        manage = GridLayout()
        manage.cols = 3

        manage.add_widget(Button(text='save', on_release=self.on_save))
        manage.add_widget(Button(text='cancel', on_release=self.cancel))
        manage.add_widget(Button(text='delete', on_release=self.on_delete))
        self.content.add_widget(manage)

    def on_save(self, instance):
        callback = pl.RePlanning()
        callback.updated_simple_tasks.append((self.__task, self.create_task()))
        self.__callback(callback, redraw=True)
        self.dismiss()

    def on_delete(self, instance):
        callback = pl.RePlanning()
        callback.removed_simple_tasks.append(self.__task)
        self.__callback(callback, redraw=True)
        self.dismiss()
