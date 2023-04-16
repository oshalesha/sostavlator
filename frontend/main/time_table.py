from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup

import frontend.constructors.buttons as btn
import scheduling.planning as pl
from frontend.design.support import empty_space


class TimeTable(GridLayout):
    def __init__(self, callback, **kwargs):
        super().__init__(**kwargs)
        self.__callback = callback
        # TODO: just a magic number ? :)
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
        # TODO: what if tasks would be more than spaces?..

        self.clear_widgets()
        # add button
        add_btn = btn.AddSimpleTaskButton(callback=self.update_plan)
        add_btn.text = "add"
        self.add_widget(add_btn)

        # real tasks
        for task in self.__plan.simple_tasks:
            self.add_widget(btn.SimpleTaskButton(task, callback=self.update_plan))

        # empty spaces
        for i in range(self.__tasks__max - len(self.__plan.simple_tasks)):
            self.add_widget(empty_space())

        # Notes button
        note_btn = Button()
        note_btn.text = "open notes"
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
            self.content.add_widget(empty_space())
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
