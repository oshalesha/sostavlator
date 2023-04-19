from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label


def empty_space(color=None):
    # TODO: there should be something clever
    if color is None:
        color = [0, 0, 0, 0]
    btn = Button()
    btn.background_color = color
    return btn


def error_window(error: str):
    window = Popup()
    window.size_hint = (0.5, 0.5)
    window.title = ""
    window.content = Label()
    window.content.text = error
    window.open()
