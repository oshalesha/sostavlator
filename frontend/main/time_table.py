from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.image import Image

import frontend.constructors.buttons as btn
import scheduling.planning as pl
import frontend.design.support as support


class TimeTable(GridLayout, Image):
    def __init__(self, callback, **kwargs):
        super().__init__(**kwargs)
        self.__callback = callback
        self.__tasks__max = 9
        # tasks + add_button + open_notes_button
        self.rows = self.__tasks__max + 2

        self.__plan = pl.Plan()
        self.__redraw()

    def show(self, plan: pl.Plan):
        self.__plan = plan
        self.__redraw()

    def update_plan(self, callback, redraw=True):
        self.__plan = callback.shape(self.__plan)
        if redraw:
            self.__redraw()
        self.__callback(callback)

    def __redraw(self):
        self.clear_widgets()
        self.__plan.simple_tasks.sort(key=lambda task: task.get_scheduled())
        # add button
        add_btn = btn.AddSimpleTaskButton(callback=self.update_plan)
        add_btn.size_hint = (1, 2.3)
        if len(self.__plan.simple_tasks) == self.__tasks__max:
            add_btn.on_press = (lambda : support.error_window("Sorry, you reach limit for tasks"))
        self.add_widget(add_btn)

        # real tasks
        for task in self.__plan.simple_tasks:
            self.add_widget(btn.SimpleTaskButton(task, callback=self.update_plan))

        # empty spaces
        for i in range(self.__tasks__max - len(self.__plan.simple_tasks)):
            self.add_widget(support.empty_space())

        # Notes button
        note_btn = support.ButtonText()
        note_btn.text = "open notes"
        note_btn.color = [0, 0, 0, 1]
        note_btn.font_size = 28
        note_btn.bind(on_press=self.open_notes)

        self.add_widget(note_btn)

    def open_notes(self, button):
        NotesWindow(self.__plan.notes.copy(), callback=self.update_plan).open()


#########################################################################


class NotesWindow(Popup):
    def __init__(self, notes, callback, **kwargs):
        super().__init__(**kwargs)
        self.__notes = notes
        self.__callback = callback

        self.content = GridLayout()
        self.content.cols = 3
        self.content.rows = 2
        self.__redraw()

    def __redraw(self):
        self.content.clear_widgets()

        for note in self.__notes:
            self.content.add_widget(self.real_note_button(note))

        # add_button
        if len(self.__notes) < self.content.cols * self.content.rows:
            add_btn = btn.AddNoteButton(self.callback)
            add_btn.text = "add"
            self.content.add_widget(add_btn)

        # empty_spaces
        for i in range(self.content.cols * self.content.rows - 2 - len(self.__notes)):
            self.content.add_widget(support.empty_space())
        self.content.add_widget(Button(text="close", on_release=self.close))

    def real_note_button(self, note):
        btn = Button()
        btn.text = note.name
        btn.note = note
        # TODO: bind with open note
        return btn

    def callback(self, callback, redraw=True):
        self.__notes = callback.shape_notes(self.__notes)
        # no need to redraw simple tasks
        self.__callback(callback, redraw=False)
        if redraw:
            self.__redraw()

    def close(self, instance):
        self.dismiss()
