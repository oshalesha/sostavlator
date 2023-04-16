from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput


class NoteTaskConstructor:
    pass


class NoteConstructor:
    _popup: Popup
    _note_name: str
    _callback: RePlanning

    def __init__(self):
        ntc = NoteConstructor
        ntc._popup = Popup()
        ntc._note_name = TextInput()
        ntc._callback = RePlanning()

    def window(self):
        # can't save it as object fields due to kivy popup behavior
        ntc = NoteConstructor

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
        ntc = NoteConstructor
        if ntc._note_name.text == "":
            return
        ntc._callback.added_notes.append(ntc._note_name.text)
        NoteConstructor._popup.dismiss()

    @staticmethod
    def cancel(button):
        NoteConstructor._popup.dismiss()

    def callback(self):
        return NoteConstructor._callback
