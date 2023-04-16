from kivy.app import App
from kivy.uix.gridlayout import GridLayout

import core.manager as mn


class MainApp(App):
    def build(self):
        self.title = 'sostavlator'
        return mn.Manager()


if __name__ == "__main__":
    MainApp().run()
