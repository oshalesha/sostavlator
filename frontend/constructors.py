from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup

from scheduling.planning import NoteTask, SimpleTask, Plan, Note

from typing import Any
from enum import Enum
from abc import ABC, abstractmethod


class Constructor(ABC):
    @abstractmethod
    def window(self):
        raise NotImplementedError()

    @abstractmethod
    def callback(self):
        raise NotImplementedError()

#############################################################


class SimpleTaskConstructor(Constructor):

    def window(self):
        return Popup()

    def callback(self):
        return CallBack()


#############################################################


class NoteTaskEditor(Constructor):

    def window(self):
        return Popup()

    def callback(self):
        return CallBack()


#############################################################


class NoteTaskConstructor(Constructor):
    def window(self):
        return Popup()

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