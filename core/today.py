from datetime import date

current_date = date.today()


def today():
    return current_date


def set_date(day):
    globals()['current_date'] = day
