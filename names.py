from datetime import datetime
import sys
import csv


class MarkCell:  # marcello
    def __init__(self, position: int, name: str, frequency: int, category: str, importance: str):
        self.__position = position
        self.__name = name
        self.__frequency = frequency
        self.__category = category
        self.__importance = importance

    def get_position(self):
        return self.__position

    def get_name(self):
        return self.__name

    def get_frequency(self):
        return self.__frequency

    def get_category(self):
        return self.__frequency

    def get_importance(self):
        return self.__importance

class CheckMarkCell(MarkCell):  # ячейка в списке продуктов (с галочками)
    def __init__(self, check_mark=False, **kwargs):
        super().__init__(**kwargs)
        self.__check_mark = check_mark

    def get_check_mark(self):
        return self.__check_mark


class DateMarkCell(MarkCell):  # ячейка в временном списке
    def __init__(self, date_time=datetime.now(), **kwargs):
        self.__date_time = date_time
        super().__init__(**kwargs)

    def get_date_time(self):
        return self.__date_time

