import csv
from datetime import datetime
from os import path
import os
from CellObjects import CheckMarkCell


def get_pos(yanked, cell):
    for pos in range(len(yanked)):
        if CheckMarkCell(*yanked[pos]).get_action() == cell.get_action():
            return pos
    return None


class NotesManager:
    def __init__(self):
        self.__file_name = '__notes.csv'
        if not path.exists(self.__file_name):
            f = open(self.__file_name, mode='x')
            f.close()

    def get_yanked(self):
        with open(self.__file_name, mode='r') as f:
            yanked = [row for row in csv.reader(f)]
        return yanked

    def write_yanked(self, yanked: list):
        with open(self.__file_name, mode='w') as f:
            writer = csv.writer(f)
            writer.writerows(yanked)

    def exists(self, name: str):
        yanked = self.get_yanked()
        for pos in range(len(yanked)):
            if yanked[pos][0] == name:
                return pos
        return None

    def remove(self, name):  # удалятор
        yanked = self.get_yanked()
        index = self.exists(name=name)
        del yanked[index]
        if path.exists(name + '.csv'):
            os.remove(name + '.csv')
        self.write_yanked(yanked=yanked)
        return index

    def add(self, name: str):
        yanked = self.get_yanked()
        index = self.exists(name=name)
        if index is None:
            f = open(name + '.csv', mode='x')
            f.close()
            yanked.insert(len(yanked), [name])
            self.write_yanked(yanked=yanked)


class CheckMarkLogger:  # should be a child of the abstract class 'Logger'
    def __init__(self, note_name):
        self.__file_name = note_name + '.csv'
        if not path.exists(self.__file_name):
            f = open(self.__file_name, mode='x')
            f.close()
        notes_manager = NotesManager()
        notes_manager.add(note_name)

    def get_file_name(self):
        return self.__file_name

    def get_check_mark_cell(self, index=0):
        with open(self.__file_name, mode='r') as f:
            yanked = [row for row in csv.reader(f)]
            return CheckMarkCell(*yanked[index])  # cast to check mark cell

    def get_yanked(self):
        with open(self.__file_name, mode='r') as f:
            yanked = [row for row in csv.reader(f)]
        return yanked

    def write_yanked(self, yanked: list):
        with open(self.__file_name, mode='w') as f:
            writer = csv.writer(f)
            writer.writerows(yanked)

    def exists(self, name: str):
        yanked = self.get_yanked()
        for task in yanked:
            if CheckMarkCell(*task).get_action() == name:
                return True
        return False

    def remove_check_mark_cell(self, cell: CheckMarkCell):  # удалятор
        yanked = self.get_yanked()
        index = get_pos(yanked, cell)
        del yanked[index]
        self.write_yanked(yanked=yanked)
        return index

    def add_check_mark_cell(self, cell: CheckMarkCell):
        yanked = self.get_yanked()
        index = get_pos(yanked, cell)
        if index is None:
            yanked.insert(len(yanked), cell.to_list())
            self.write_yanked(yanked=yanked)

    def update_check_mark_cell(self, old_cell: CheckMarkCell, new_cell: CheckMarkCell):
        if self.exists(name=new_cell.get_action()) and self.exists(
                name=old_cell.get_action()) and new_cell.get_action() != old_cell.get_action():
            raise "You cannot save it as an existing name."
        if old_cell.get_action() == new_cell.get_action() and old_cell.get_status() and new_cell.get_status() is False:
            calls = new_cell.get_calls_number()
            interval = (datetime.now() - new_cell.get_date_time()).total_seconds() / 3600
            new_cell.set_period((calls * new_cell.get_period() + interval) / (calls + 1))
            new_cell.set_date_time(datetime.now())
            new_cell.set_calls_number(calls + 1)
        self.remove_check_mark_cell(cell=old_cell)
        self.add_check_mark_cell(cell=new_cell)

    def clear(self):
        self.write_yanked(yanked=[])

    def pull_out(self):
        yanked = self.get_yanked()
        cells = [CheckMarkCell(*cell) for cell in yanked]
        return cells


class TimeLogger:
    def __init__(self, dir_name):
        self.__dir_name = dir_name
        if not path.exists(self.__dir_name):
            os.mkdir(dir_name)
            for i in range(1, 13):
                f = open('./' + dir_name + '/' + str(i) + '.csv', mode='x')
                f.close()
            notes_manager = NotesManager()
            notes_manager.add(dir_name)

    def get_dir_name(self):
        return self.__dir_name

    def get_yanked(self, month: int):
        with open(self.__dir_name + '/' + str(month) + '.csv', mode='r') as f:
            yanked = [row for row in csv.reader(f)]
        return yanked
