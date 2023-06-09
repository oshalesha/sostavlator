from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label


import scheduling.planning as pl


images = 'frontend/design/pictures/'


def empty_space(color=None):
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


def black_line():
    return Image(source=images + 'black_line.png')


def simple_task_status_image(task: pl.SimpleTask):
    file = ""
    imp = task.get_importance().value
    if task.get_status():
        file = 'done.png'
    elif imp == 0:
        file = 'white_circle.png'
    elif imp == 1:
        file = 'yellow_circle.png'
    elif imp == 2:
        file = 'orange_circle.png'
    else:
        file = 'red_circle.png'
    return images + file


def note_tasks_status_image(task: pl.NoteTask):
    if task.get_status():
        return images + 'done.png'
    return images + 'white_circle.png'


def plus_image():
    return images + 'plus.jpg'


def back_image():
    return images + 'back.png'


class ButtonImage(ButtonBehavior, Image):
    pass


class ButtonText(ButtonBehavior, Label):
    pass


class ImageLayout(GridLayout, Image):
    pass

