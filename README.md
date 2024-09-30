# SOSTAVLATOR

```Sostavlator``` is an application that allows you to create a schedule using suggested prompts.

## Functions

## `Getting Started`
When you first launch, you will be asked to answer a few simple questions to customize the tips
specifically for you. Our app will compare your answers with the information we collected through a survey.
The survey is short, but it will make your future use of the app much more enjoyable.


## `Main menu`
The main menu looks like this:

![tutorial_1](frontend/design/pictures/tutorial_1.jpg)


You can select the day for which you are making a schedule, create tasks for this day, edit them, and mark them as completed. The color of the circle next to the task determines its importance, the color of the task itself determines its category. Deleting a task is available in its editing mode.

## `Creating a task`

When creating, you enter the name of the task, define its category and importance, as well as the desired time. Do not worry
about entering something incorrectly - the application itself will prompt you in case of an error. On the right are buttons with
hints - when pressed, the task name is entered into the name line.

![tutorial_2](frontend/design/pictures/tutorial_2.jpg)

## `Suggestion system`

If you are making a schedule and have not managed to include enough different activities, then ```Compiler``` will suggest the activities that you would most likely prefer to do based on a ML algorithm, based on your characteristics.

Don't worry if the app prompts you with seemingly arbitrary tasks at first. Over time,
it will learn and adapt to you. The longer you use the app, the more accurate the prompts become


## `Installation`

To run the application, just clone the repository, download all the necessary libraries -
the simplest solution here is to write ```pip install -r requirements.txt``` from the repository root. Then, just run the [main.py](main.py) file.

Linux users should comment out the line ```%(name)s = probesysfs``` in the ```[input]``` section
in the ```~/.kivy/config.ini``` file.

This is due to a rather [strange, long-known behavior of kivy](https://stackoverflow.com/questions/59963631/python-kivy-on-press-being-executed-twice).


## `Future`

To-do lists are also being developed now, which will not depend on the day, with their own system of hints: to suggest
objects that have not been marked as completed for a long time. An ideal example of its application is a grocery list.
