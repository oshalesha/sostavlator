from kivy.uix.button import Button


def empty_space(color=None):
    # TODO: there should be something more clever
    if color is None:
        color = [0, 0, 0, 0]
    btn = Button()
    btn.background_color = color
    return btn
