import csv
import pandas as pd
from braid import *


class FamilyParser:

    def __init__(self, csv_file):
        self.raw_csv = open(csv_file, newline='', encoding='utf-8-sig')
        self.family_data = csv.DictReader(self.raw_csv)
        self.family_members = None
        self.birthdays = None

    def __del__(self):
        self.raw_csv.close()

    def __next__(self):
        return next(self.family_data)

    def get_family_members(self):
        if self.family_members is None:
            self.family_members = []
            for member in self.family_data:
                self.family_members.append(FamilyMember(member))
        return self.family_members

    def get_month_sorted_family(self):
        if self.family_members is None:
            self.get_family_members()
        return sorted(self.family_members, key=lambda x: x.get_birth().month)


class FamilyMember:

    def __init__(self, infoDict):
        self.birth = pd.to_datetime(infoDict["Birth"], dayfirst=True)
        self.death = pd.to_datetime(infoDict["Death"], dayfirst=True)
        self.reference_num = int(infoDict["Reference Number"])
        self.name = infoDict["Name"]
        self.thread = None

    def get_ref_num(self):
        return self.reference_num

    def get_name(self):
        return self.name

    def get_birth(self):
        return self.birth

    def get_death(self):
        return self.death

    def set_braid_thread(self, thread):
        self.thread = thread

    def get_thread(self):
        return self.thread

    def passed(self, year):
        if pd.isnull(self.death) or self.death.year > year:
            return False
        elif self.death.year == year:
            self.thread.chord = E2, DOM
            self.thread.velocity = 1
        return True

