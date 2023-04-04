from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.pickers import MDDatePicker
from kivy.uix.popup import Popup


class NoteDialog(Popup):
    note_text = ""


class MainApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "BlueGray"
        return Builder.load_file('my.kv')

    def show_date_picker(self):
        date_dialog = MDDatePicker()
        date_dialog.open()

    def show_note_dialog(self):
        self.note_dialog = NoteDialog()
        self.note_dialog.ids.note_text.text = ""
        self.note_dialog.open()

    def save_note(self):
        note_text = self.note_dialog.ids.note_text.text
        NoteDialog.note_text = note_text
        self.note_dialog.dismiss()


'''
    def save_note(self):
        note_text = self.root.ids.note_text.text
        # Save the note to a file or database
        self.root.ids.note_text.text = ""
        '''

MainApp().run()
