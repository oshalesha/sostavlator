from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

import frontend.design.support as support
import Loggers.Loggers.Loggers as loggers


class Hello(support.ImageLayout):
    def __init__(self, end, **kwargs):
        super().__init__(**kwargs)
        self.rows = 2
        self.end = end
        self.add_widget(Label(text="Hi, to improve the hint system, \n"
                                           "our team offers you to answer a few \n"
                                           "simple questions. It won't take long.",
                                      font_size=42, color=(0, 0, 0, 1)))
        self.add_widget(Button(text="go", font_size=84, color=(0, 1, 0, 1), on_press=self.go))

        self.sex = 'M'
        self.age = TextInput(hint_text="Your age", font_size=48)
        self.free_time = TextInput(hint_text="Free time from 0 to 10", font_size=48)

        self.men_btn = support.ButtonText(text="Men", color=(1, 0, 0, 1), font_size=48, on_press=self.men)
        self.women_btn = support.ButtonText(text="Women", color=(0, 0, 0, 1), font_size=38, on_press=self.women)
        self.movies_btn = support.ButtonText(text="movies", color=(0, 0, 0, 1), font_size=38,
                                             on_press=self.change_choose)
        self.reading_btn = support.ButtonText(text="reading", color=(0, 0, 0, 1), font_size=38,
                                              on_press=self.change_choose)
        self.art_btn = support.ButtonText(text="art", color=(0, 0, 0, 1), font_size=38,
                                          on_press=self.change_choose)
        self.studying_btn = support.ButtonText(text="studying", color=(0, 0, 0, 1), font_size=38,
                                               on_press=self.change_choose)
        self.activities_btn = support.ButtonText(text="activities", color=(0, 0, 0, 1), font_size=38,
                                                 on_press=self.change_choose)
        self.sport_btn = support.ButtonText(text="sport", color=(0, 0, 0, 1), font_size=38,
                                            on_press=self.change_choose)
        self.work_btn = support.ButtonText(text="work", color=(0, 0, 0, 1), font_size=38,
                                           on_press=self.change_choose)

        self.studying_btn.value = False
        self.activities_btn.value = False
        self.movies_btn.value = False
        self.work_btn.value = False
        self.sport_btn.value = False
        self.art_btn.value = False
        self.reading_btn.value = False

    def go(self, instance):
        self.clear_widgets()
        self.rows = 5
        self.add_widget(Label(text="Select your sex", color=(0, 0, 0, 1), font_size=48))

        sex_manage = support.ImageLayout(cols=2)
        sex_manage.add_widget(self.men_btn)
        sex_manage.add_widget(self.women_btn)
        self.add_widget(sex_manage)

        self.add_widget(self.age)
        self.add_widget(self.free_time)
        self.add_widget(Button(text="next", font_size=64, color=(0, 1, 0, 1), on_press=self.second_step))

    def men(self, instance):
        self.sex = 'M'
        self.men_btn.color = (1, 0, 0, 1)
        self.men_btn.font_size = 48
        self.women_btn.color = (0, 0, 0, 1)
        self.women_btn.font_size = 38

    def women(self, instance):
        self.sex = 'W'
        self.men_btn.color = (0, 0, 0, 1)
        self.men_btn.font_size = 38
        self.women_btn.color = (1, 0, 0, 1)
        self.women_btn.font_size = 48

    def second_step(self, instance):
        if not str(self.age.text).isnumeric():
            support.error_window("it seems you entered the wrong age")
            return
        if not str(self.free_time.text).isnumeric():
            support.error_window("it seems you entered the wrong free time")
            return
        if not (10 >= int(self.free_time.text) >= 0):
            support.error_window("it seems you entered the wrong free time")
            return

        self.clear_widgets()
        self.rows = 9
        self.add_widget(Label(text="Choose your interests", color=(0, 0, 0, 1), font_size=48))
        self.add_widget(self.studying_btn)
        self.add_widget(self.activities_btn)
        self.add_widget(self.sport_btn)
        self.add_widget(self.work_btn)
        self.add_widget(self.movies_btn)
        self.add_widget(self.art_btn)
        self.add_widget(self.reading_btn)
        self.add_widget(support.ButtonText(text="finish", font_size=64,
                                                   color=(0, 1, 0, 1), on_press=self.finish))

    def change_choose(self, instance):
        instance.value = not instance.value
        if instance.value:
            self.change_to_choose(instance)
        else:
            self.change_to_not_choose(instance)

    def change_to_choose(self, btn):
        btn.font_size = 48
        btn.color = (1, 0, 0, 1)

    def change_to_not_choose(self, btn):
        btn.font_size = 38
        btn.color = (0, 0, 0, 1)

    def finish(self, instance):
        loggers.PersonalLogger(sex=self.sex, age=int(self.age.text), free_time=float(self.age.text)/10,
                               picked_movies=self.movies_btn.value, picked_art=self.art_btn.value,
                               picked_work=self.work_btn.value, picked_studying=self.studying_btn.value,
                               picked_sports=self.sport_btn.value, picked_reading=self.reading_btn.value,
                               picked_activities=self.activities_btn.value)
        self.end()
