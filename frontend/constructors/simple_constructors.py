from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label

import scheduling.planning as pl
import core.today as td
import frontend.design.support as support
import frontend.design.colors as colors
import Oracle.Oracle as orcl

from datetime import datetime


def importance_name(importance):
    name = str(pl.Importance(importance).name)
    name = name.replace('_', ' ')
    return name


def category_name(category):
    name = pl.Category(category).name
    name = name.replace('_', ' ')
    return name


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
        self.title = ""
        self.content = GridLayout()
        self.content.rows = 3

        # create main part
        self._task_name = TextInput(multiline=False)
        self._task_name.hint_text = "name your task"
        self._task_name.font_size = 32

        self._category = 0
        self._importance = 0

        self._importance_btn = support.ButtonText()
        self._importance_btn.text = importance_name(self._importance)
        self._importance_btn.font_size = 40
        self._importance_btn.on_release = self.change_importance
        self.update_importance()

        self._category_btn = support.ButtonText()
        self._category_btn.text = category_name(self._category)
        self._category_btn.font_size = 40
        self._category_btn.on_release = self.change_category
        self.update_category()

        self._time_minute = TextInput(multiline=False)
        self._time_minute.hint_text = "minutes"
        self._time_minute.font_size = 42

        self._time_hours = TextInput(multiline=False)
        self._time_hours.hint_text = "hours"
        self._time_hours.font_size = 42

        # push everything in content
        self.content.add_widget(self._task_name)
        # category and importance
        configs = GridLayout()
        configs.cols = 2
        configs.add_widget(self._category_btn)
        configs.add_widget(self._importance_btn)
        self.content.add_widget(configs)
        # hours and minutes
        time = GridLayout()
        time.cols = 2
        time.add_widget(self._time_hours)
        time.add_widget(self._time_minute)
        self.content.add_widget(time)

    def create_task(self):
        if self._task_name.text == "":
            support.error_window("you have to name the task somehow :)")
            return None
        elif not self.valid_time():
            support.error_window("it seems that you entered the not correct time")
            return None

        today = td.today()
        timer = datetime(today.year, today.month, today.day,
                         int(self._time_hours.text), int(self._time_minute.text))
        return pl.SimpleTask(action=self._task_name.text, category=pl.Category(self._category),
                             scheduled=timer,
                             importance=pl.Importance(self._importance), status=False)

    def valid_time(self):
        minute = str(self._time_minute.text)
        hours = str(self._time_hours.text)
        if not minute.isnumeric() or not hours.isnumeric():
            return False
        if not 0 <= int(minute) <= 59 or not 0 <= int(hours) <= 23:
            return False
        return True

    def change_importance(self):
        if self._importance == len(pl.Importance) - 1:
            self._importance = 0
        else:
            self._importance += 1
        self.update_importance()

    def update_importance(self):
        self._importance_btn.text = importance_name(self._importance)
        self._importance_btn.color = colors.task_importance_color(self._importance)

    def change_category(self):
        if self._category == len(pl.Category) - 1:
            self._category = 0
        else:
            self._category += 1
        self.update_category()

    def update_category(self):
        self._category_btn.text = category_name(self._category)
        self._category_btn.color = colors.task_category_color(self._category, theme="black")

    def cancel(self, instance):
        self.dismiss()


#########################################################


class SimpleTaskConstructor(SimpleTaskCntWindow):
    def __init__(self, callback, **kwargs):
        super().__init__(**kwargs)
        self.__callback = callback

        self.content.rows += 1
        manage = GridLayout()
        manage.cols = 2
        # add manage menu
        self.content.rows += 1
        manage = GridLayout()
        manage.cols = 2

        manage.add_widget(support.ButtonText(text='save', on_release=self.on_save, font_size=42, color=(0, 1, 0, 1)))
        manage.add_widget(support.ButtonText(text='cancel', on_release=self.cancel, font_size=42))
        self.content.add_widget(manage)

        # add hints window
        simple_content = self.content
        self.content = GridLayout(cols=2)
        self.content.add_widget(SimpleHintsWindow(self))
        self.content.add_widget(simple_content)
        simple_content.size_hint = (1.8, 1)

        self.size_hint = (0.8, 1)
        self.pos_hint = {'x': 0.1, 'y': 0}

    def on_save(self, instance):
        callback = pl.RePlanning()
        task = self.create_task()
        if task is None:
            # error in user input
            return
        callback.added_simple_tasks.append(self.create_task())
        self.__callback(callback, redraw=True)
        self.dismiss()


##########################################################################


class SimpleHintsWindow(GridLayout):
    def __init__(self, current_cns: SimpleTaskConstructor, **kwargs):
        super().__init__(**kwargs)
        self.__cns = current_cns

        self.add_widget(Label(text="Maybe that's what\n you wanted to do", font_size=24))

        hints = orcl.TimeOracle().predict()
        self.rows = len(hints) + 1
        for hint in hints:
            self.add_widget(self.hint_button(hint))

    def hint_button(self, name: str):
        btn = Button(text=name, font_size=24)

        def press(instance):
            self.__cns._task_name.text = btn.text

        btn.bind(on_press=press)
        return btn


##########################################################################


class SimpleTaskRedactor(SimpleTaskCntWindow):
    def __init__(self, callback, task: pl.SimpleTask, **kwargs):
        super().__init__(**kwargs)
        self.__task = task
        self.__callback = callback
        self.size_hint = (0.7, 0.9)
        self.pos_hint = {'x': 0.15, 'y': 0.05}

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

        manage.add_widget(support.ButtonText(text='save', on_release=self.on_save, font_size=42, color=(0, 1, 0, 1)))
        manage.add_widget(support.ButtonText(text='cancel', on_release=self.cancel, font_size=42))
        manage.add_widget(support.ButtonText(text='delete', on_release=self.on_delete, font_size=42, color=(1, 0, 0, 1)))
        self.content.add_widget(manage)

    def on_save(self, instance):
        callback = pl.RePlanning()
        task = self.create_task()
        task.set_status(self.__task.get_status())

        if task is None:
            # error in user input
            return
        callback.updated_simple_tasks.append((self.__task, task))
        self.__callback(callback, redraw=True)
        self.dismiss()

    def on_delete(self, instance):
        callback = pl.RePlanning()
        callback.removed_simple_tasks.append(self.__task)
        self.__callback(callback, redraw=True)
        self.dismiss()
