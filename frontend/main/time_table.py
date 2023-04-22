from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.uix.label import Label

import frontend.constructors.buttons as btn
import scheduling.planning as pl
import frontend.design.support as support


class TimeTable(GridLayout, Image):
    def __init__(self, callback, **kwargs):
        super().__init__(**kwargs)
        self.__callback = callback
        self.__tasks__max = 9
        # tasks + add_button + open_notes_button
        self.rows = self.__tasks__max + 1

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
            add_btn.on_press = (lambda: support.error_window("Sorry, you reach limit for tasks"))
        self.add_widget(add_btn)

        # real tasks
        for task in self.__plan.simple_tasks:
            self.add_widget(btn.SimpleTaskButton(task, callback=self.update_plan))

        # empty spaces
        for i in range(self.__tasks__max - len(self.__plan.simple_tasks)):
            self.add_widget(support.black_line())

        '''# Notes button
        note_btn = support.ButtonText(text="open notes", color=[0, 0, 0, 1], font_size=46, size_hint=(1, 1.4))
        note_btn.bind(on_press=self.open_notes)

        self.add_widget(note_btn)'''

    def open_notes(self, button):
        NotesTable(self.__plan.notes.copy(), callback=self.update_plan).open()


#########################################################################


class NotesTable(Popup):
    def __init__(self, notes, callback, **kwargs):
        super().__init__(**kwargs)
        self.__notes = notes
        self.__callback = callback

        self.content = support.ImageLayout()
        self.content.cols = 3
        self.content.rows = 2
        self.__redraw()

    def __redraw(self):
        self.content.clear_widgets()

        for note in self.__notes:
            self.content.add_widget(self.open_note_button(note))

        # add_button
        if len(self.__notes) < self.content.cols * self.content.rows:
            add_btn = btn.AddNoteButton(self.update)
            add_btn.source = support.plus_image()
            self.content.add_widget(add_btn)

        # empty_spaces
        for i in range(self.content.cols * self.content.rows - 2 - len(self.__notes)):
            self.content.add_widget(support.empty_space())

        # back_button
        self.content.add_widget(support.ButtonImage(source=support.back_image(), on_release=self.dismiss))

    def open_note_button(self, note):
        button = support.ButtonText(text=note.name, color=(0, 0, 0, 1), font_size=32)
        button.on_release = lambda: NoteWindow(note, callback=self.update).open()
        return button

    def update(self, callback, redraw=True):
        self.__notes = callback.shape_notes(self.__notes)
        # no need to redraw simple tasks
        self.__callback(callback, redraw=False)
        if redraw:
            self.__redraw()


#########################################################################


class NoteWindow(Popup):
    def __init__(self, note: pl.Note, callback, **kwargs):
        super().__init__(**kwargs)
        self.__note = note
        self.__callback = callback
        self.content = support.ImageLayout(rows=2)

        # manage menu
        back = support.ButtonImage(source=support.back_image())
        back.on_press = self.dismiss

        manage = support.ImageLayout(cols=3)
        manage.add_widget(btn.AddNoteTaskButton(note=note, callback=self.update))
        manage.add_widget(btn.NoteLabel(name=note.name, callback=self.update))
        manage.add_widget(back)

        # hints + tasks
        hints_table = GridLayout(rows=2)
        hints_table.add_widget(Label(text="Perhaps you need it now"))
        self.hints = GridLayout()
        hints_table.add_widget(self.hints)

        self.tasks = support.ImageLayout()

        table = GridLayout(cols=2)
        table.add_widget(hints_table)
        table.add_widget(self.tasks)

        # push
        self.content.add_widget(manage)
        self.content.add_widget(table)

        # draw
        self.redraw_tasks()
        self.redraw_hints()

    def update(self, callback, close=True, redraw_tasks=True, redraw_hints=True):
        self.__note = callback.shape_notes([self.__note])[0]
        self.__callback(callback)
        if close:
            self.dismiss()
            return
        if redraw_tasks:
            self.redraw_tasks()
        if redraw_hints:
            self.redraw_hints()

    def redraw_tasks(self):
        pass

    def redraw_hints(self):
        pass
