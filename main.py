from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

import core.manager as mn
from frontend.welcome.hello import Hello
import FirstTimeRunning.FirstTimeRunning as first


class MainApp(App, BoxLayout):
    def build(self):
        self.title = 'sostavlator'
        if first.FirstTimeRunning().first_time_running():
            self.add_widget(Hello(end=self.create_app))
        else:
            self.create_app()
        return self

    def create_app(self):
        self.clear_widgets()
        self.add_widget(mn.Manager())


if __name__ == "__main__":
    MainApp().run()

