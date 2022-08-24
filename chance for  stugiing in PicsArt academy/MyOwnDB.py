import os
import json

import openpyxl
import pandas as pd
from datetime import date
import time


class MyOwnDB(object):
    def __init__(self, location):
        self.location = os.path.expanduser(location)
        self.load(self.location)

    def load(self, location):
        if os.path.exists(location):
            self._load()
        else:
            self.db = {}
        return True

    def _load(self):
        try:
            self.db = json.load(open(self.location, "r"))
        except:
            self.db = {}

    def dumpDB(self):
        try:
            json.dump(self.db, open(self.location, "w+"))
            return True
        except:
            return False

    def set(self, key, value):
        try:
            self.db[str(key)] = value
            self.dumpDB()
            return True
        except Exception as e:
            print("[X] Error Saving Values to Database : " + str(e))
            return False

    def get(self, key):
        try:
            return self.db[key]
        except KeyError:
            print("No Value Can Be Found for " + str(key))
            return False

    def delete(self, key):
        if key not in self.db:
            print("Error no such key in db")
            return False
        del self.db[key]
        self.dumpDB()
        return True

    def resetDB(self):
        self.db = {}
        self.dumpDB()
        return True

    def exist(self, key):
        if self.db.__contains__(key):
            return True
        else:
            return False

    def changeValue(self, key, value):
        self.db[key] = value
        self.dumpDB()
        return True

    def append(self, key, value):
        if self.exist(key):
            old_values = [self.db.get(key)]
            old_values.append(value)
            self.db[key] = old_values
        else:
            self.set(key, value)

    def changeKey(self, oldKey, newKey):
        value = self.db[oldKey]
        self.delete(oldKey)
        self.set(newKey, value)

    def sortByKeys(self):
        return sorted(self.db.keys())

    def sortByValues(self):
        return sorted(self.db.values())

    def type(self, key):
        value = (self.db[key])
        return type(value)

    def allItems(self):
        return self.db

    def update_excel(self, filename):
        book = openpyxl.load_workbook('%s.xlsx' % filename)
        sheet = book.active
        free_column = int(sheet.max_row) + 1
        alf = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O']
        value = 0
        string = str(self.db.values())[13:-2]
        values = string.split(',')
        for elem in alf:
            key = str(elem) + str(free_column)
            sheet[key] = values[value]
            value += 1
        book.save('%s.xlsx' % filename)

    def to_excel(self, filename):
        data = [self.db]
        data_frame = pd.DataFrame(data)
        writer = pd.ExcelWriter('%s.xlsx' % filename, engine='xlsxwriter')
        data_frame.to_excel(writer, sheet_name=date.today().strftime("%B %d, %Y"), index=False)
        writer.save()

    def percentage(self):
        try:
            values = list(self.db.values())
            amount = float(sum(values))
            keys = list(self.db.keys())
            percentage = {}
            i = 0
            for val in values:
                key = keys[i]
                percent = (val / amount) * 100
                percentage[key] = round(percent, 1)
                i += 1
            return list(percentage.items())
        except Exception as e:
            return False
