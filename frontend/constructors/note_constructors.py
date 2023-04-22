from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput

import scheduling.planning as pl


class NoteConstructor(Popup):
    def __init__(self, callback, **kwargs):
        super().__init__(**kwargs)
        self.__callback = callback
        self.__note__name = TextInput()

        self.content = GridLayout()
        self.content.rows = 2

        self.content.add_widget(self.__note__name)
        manage = GridLayout()
        manage.cols = 2
        manage.add_widget(Button(text="save", on_release=self.save))
        manage.add_widget(Button(text="cancel", on_release=self.cancel))
        self.content.add_widget(manage)

    def save(self, button):
        if self.__note__name.text == "":
            return
        callback = pl.RePlanning()
        callback.added_notes.append(self.__note__name.text)
        self.__callback(callback, redraw=True)
        self.dismiss()

    def cancel(self, button):
        self.dismiss()

##########################################################


class NoteRedactor:
    pass

##########################################################


class NoteTaskConstructor:
    pass


##########################################################
class NoteTaskRedactor:
    pass
