from datetime import datetime


def to_time(string: str):
    return datetime.strptime(string, '%Y-%m-%d %H:%M:%S.%f')


class MarkCell:
    def __init__(self, action="", status=False):
        self.__action = action
        self.__status = status

    def get_action(self):
        return self.__action

    def get_status(self):
        return self.__status

    def set_action(self, new_action=""):
        self.__action = new_action

    def set_status(self, new_status=""):
        self.__status = new_status

    def to_list(self):
        return list(vars(self).values())

    def __str__(self):
        return str(list(vars(self).values()))


class CheckMarkCell(MarkCell):
    def __init__(self, period=0, calls_number=0, date_time=datetime.now(), action="", status=False):
        self.__period = period  # check the default value later
        self.__calls_number = calls_number
        self.__date_time = date_time
        super().__init__(action=action, status=status)

    def get_calls_number(self):
        return self.__calls_number

    def get_period(self):
        return self.__period

    def get_date_time(self):
        return self.__date_time

    def set_calls_number(self, new_calls_number=0):
        self.__calls_number = new_calls_number
        return self

    def set_period(self, new_period=0):
        self.__period = new_period
        return self

    def set_date_time(self, new_date_time=datetime.now()):
        self.__date_time = new_date_time
        return self

