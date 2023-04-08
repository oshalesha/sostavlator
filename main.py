from kivy.app import App
from kivy.uix.gridlayout import GridLayout

from frontend.my_calendar import Calendar
from frontend.time_table import TimeTable
from settings.settings import Settings


class MainApp(App):
    def build(self):
        main_window = GridLayout()
        main_window.cols = 2
        main_window.add_widget(Settings())

        interface_window = GridLayout()
        interface_window.cols = 2
        interface_window.add_widget(TimeTable())
        interface_window.add_widget(Calendar.window())

        main_window.add_widget(interface_window)
        return main_window


if __name__ == "__main__":
    MainApp().run()
