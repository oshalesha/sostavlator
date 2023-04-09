from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup

from planning import NoteTask, SimpleTask, Plan

import enum


class SimpleTaskConstructor:
    def window(self):
        pass

#############################################################


class NoteTaskEditor:
    def window(self):
        pass


#############################################################


class NoteTaskConstructor:
    def window(self):
        pass

#############################################################


class CallBack:
    class TYPE(enum):
        Note = 0,
        NoteTask = 1,
        SimpleTask = 2

    class CHANGE(enum):
        Add = 0,
        Update = 1,
        Remove = 2
