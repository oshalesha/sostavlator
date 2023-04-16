from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, Rectangle


def empty_space(color=None):
    # TODO: there should be something clever
    if color is None:
        color = [0, 0, 0, 0]
    btn = Button()
    btn.background_color = color
    return btn