from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label


import scheduling.planning as pl


images = 'frontend/design/pictures/'


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


def task_status_image(task: pl.SimpleTask):
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


def task_category_color(task: pl.SimpleTask):
    cat = task.get_category().value
    if cat == 0:
        return 1, 0, 0, 1
    elif cat == 1:
        return 0, 1, 0, 1
    elif cat == 2:
        return 0, 0, 1, 1
    elif cat == 3:
        return 1, 1, 0, 1
    elif cat == 4:
        return 0, 1, 1, 1


def plus_image():
    return images + 'plus.jpg'


class ButtonImage(ButtonBehavior, Image):
    pass


class ButtonText(ButtonBehavior, Label):
    pass
