# import time
# import pandas as pd

from utils import FamilyParser
from braid import *
import copy

START_YEAR = 1990
END_YEAR = 2021


def counter(func):
    def wrapped(*args, **kwargs):
        if wrapped.year == END_YEAR:
            #stop()
            return
        wrapped.year += 1
        print(wrapped.year)
        return func(*args, wrapped.year, **kwargs)
    wrapped.year = START_YEAR - 1
    return wrapped

@counter
def update_all_patterns(curr_year):
    global family
    global_pattern = create_global_pattern(curr_year)
    for memb in family:
        memb_num = memb.get_ref_num()
        personal_pat = global_to_personal(copy.deepcopy(global_pattern), memb_num)
        memb.get_thread().pattern = personal_pat
        # 2nd version
        # update_personal_pattern

def global_to_personal(pattern, mem_num):
    for i in range(4):
        if not pattern[i]:
            pattern[i] = 0
        else:
            pattern[i] = [i if i == mem_num else 0 for i in pattern[i]]
    return pattern


def update_personal_pattern(mem, curr_year):
    q1, q2, q3, q4 = [0] * 4
    mem_thread = mem.get_thread()
    mem_birth_year = mem.get_birth().year
    mem_birth_month = mem.get_birth().month
    mem_num = mem.get_ref_num()

    if curr_year < mem_birth_year:
        pass
    else:
        if mem_birth_month in [1, 2, 3]:
            q1 = mem_num
        elif mem_birth_month in [4, 5, 6]:
            q2 = mem_num
        elif mem_birth_month in [7, 8, 9]:
            q3 = mem_num
        else:
            q4 = mem_num

    mem_thread.pattern = [q1, q2, q3, q4]
    return


def create_global_pattern(curr_year):
    global family
    q1, q2, q3, q4 = [], [], [], []
    for mem in family:
        mem_birth_year = mem.get_birth().year
        mem_birth_month = mem.get_birth().month
        mem_num = mem.get_ref_num()

        if curr_year < mem_birth_year:
            pass
        else:
            if mem_birth_month in [1, 2, 3]:
                q1.append(mem_num)
            elif mem_birth_month in [4, 5, 6]:
                q2.append(mem_num)
            elif mem_birth_month in [7, 8, 9]:
                q3.append(mem_num)
            else:
                q4.append(mem_num)

    return [q1, q2, q3, q4]


parser = FamilyParser("elazar_family.csv")
family = parser.get_month_sorted_family()

tempo(200)
family_chord = E3, DOM

global_beat = Thread(10)
global_beat.chord = family_chord
global_beat.pattern = Z, Z, Z, Z

for idx, member in enumerate(family):
    new_thread = Thread(idx + 1)
    new_thread.chord = family_chord
    new_thread.start(global_beat)
    member.set_braid_thread(new_thread)

global_beat.trigger(update_all_patterns, 1, True)
global_beat.start()
play()
