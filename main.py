from kivy.app import App

import core.manager as mn
import frontend.welcome.hello as hello


class MainApp(App):
    def build(self):
        if True:
            hello.Hello().open()
        self.title = 'sostavlator'
        return mn.Manager()


if __name__ == "__main__":
    MainApp().run()

