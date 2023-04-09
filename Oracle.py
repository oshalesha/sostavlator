from Loggers import CheckMarkLogger
from datetime import timedelta
from datetime import datetime


class CheckMarkHint:
    def __init__(self, name: str):
        self.__logger = CheckMarkLogger(name)

    def predict(self):
        hint = []
        yanked = self.__logger.get()
        for pos in range(len(yanked)):
            if timedelta(days=yanked[pos].get_period()) + yanked[pos].get_date_time() < datetime.now():
                hint.append(yanked[pos])
        return sorted(yanked, key=lambda l: l.get_calls_number(), reverse=True)[:min(5, len(yanked))]
