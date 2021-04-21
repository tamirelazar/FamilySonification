# import time
# import pandas as pd

from utils import FamilyParser
from braid import *
import copy

# START_YEAR = 1982 # keren
START_YEAR = 1990
END_YEAR = 2021
TEMPO = 200
member_passed = False
vel = 1
family_chord = E3, DOM
mourning_chord = E3, MIN


def counter(func):
    def wrapped(*args, **kwargs):
        if wrapped.year == END_YEAR:
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


@counter
def update_all_patterns_3rd(curr_year):
    global family
    global_pattern = create_global_pattern(curr_year)
    for memb in family:
        if memb.get_birth().year > curr_year:
            continue
        personal_pat = copy.deepcopy(global_pattern)
        if memb.passed(curr_year):
            update_deceased_pattern(memb, personal_pat)
        # if curr_year == 2017 and not memb.passed(curr_year):
        #     memb.thread.chord = tween((mourning_chord), 8, ease_in_out())
        else:
            memb_num = memb.get_ref_num()
            memb_thread = memb.get_thread()

            def weak(n):
                def f(memb_thread):
                    if member_passed:
                        memb_thread.velocity = 0.3
                        return n
                    else:
                        memb_thread.velocity = 0.5
                        return n
                return f

            def reg(n):
                def f(memb_thread):
                    memb_thread.velocity = 1
                    return n
                return f

            for i in range(4):
                if not personal_pat[i]:
                    personal_pat[i] = [0]
                else:
                    personal_pat[i] = [reg(i) if i == memb_num else weak(memb_num) for i in personal_pat[i]]

            memb_thread.pattern = personal_pat


def update_deceased_pattern(member, pattern):
    memb_num = member.get_ref_num()
    memb_thread = member.get_thread()

    def weak(n):
        def f(memb_thread):
            memb_thread.velocity = 0.2
            return n
        return f

    def reg(n):
        def f(memb_thread):
            global TEMPO, vel
            if TEMPO > 100:
                TEMPO = TEMPO / 4
                tempo(TEMPO)
            if vel > 0.5:
                vel = vel - 0.1
                memb_thread.velocity = vel
            # if vel <= 0.5:
            #     stop()
            #     clear()
            return n
        return f

    for i in range(4):
        if not pattern[i]:
            pattern[i] = [0]
        elif memb_num in pattern[i]:
            # pattern[i] = [weak(memb_num)]
            pattern[i] = [0]
        else:
            pattern[i] = [0]

    pattern[3].append(reg(-1))

    memb_thread.pattern = pattern


@counter
def update_all_patterns_4rd(curr_year):
    global family
    global_pattern = create_global_pattern(curr_year)
    for memb in family:
        if memb.get_birth().year > curr_year:
            continue
        memb_num = memb.get_ref_num()
        memb_thread = memb.get_thread()
        personal_pat = copy.deepcopy(global_pattern)

        def weak(n):
            def f(memb_thread):
                memb_thread.velocity = 0.8
                return n
            return f

        def reg(n):
            def f(memb_thread):
                memb_thread.velocity = 1
                return n
            return f

        for i in range(4):
            if not personal_pat[i]:
                personal_pat[i] = 0
            elif memb_num in personal_pat[i]:
                personal_pat[i] = reg(memb_num)
            else:
                personal_pat[i] = weak(memb_num)

        memb_thread.pattern = personal_pat


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

        if mem.passed(curr_year):
            global member_passed
            member_passed = True
        # if mem.passed(curr_year):
        #     death_month = mem.get_death().month
        #     mem_num = (-1) * mem_num
        #     if death_month in [1, 2, 3]:
        #         q1.append(mem_num)
        #     elif death_month in [4, 5, 6]:
        #         q2.append(mem_num)
        #     elif death_month in [7, 8, 9]:
        #         q3.append(mem_num)
        #     else:
        #         q4.append(mem_num)

    return [q1, q2, q3, q4]


data_path = "elazar_family.csv"

parser = FamilyParser(data_path)
family = parser.get_month_sorted_family()

tempo(TEMPO)

global_beat = Thread(10)
global_beat.chord = family_chord
global_beat.pattern = Z, Z, Z, Z

for idx, member in enumerate(family):
    new_thread = Thread(idx + 1)
    new_thread.chord = family_chord
    new_thread.start(global_beat)
    member.set_braid_thread(new_thread)

global_beat.trigger(update_all_patterns_3rd, 1, True)
global_beat.start()
play()







def run_sonification(data_path):
    parser = FamilyParser(data_path)
    family = parser.get_month_sorted_family()

    tempo(TEMPO)

    global_beat = Thread(10)
    global_beat.chord = family_chord
    global_beat.pattern = Z, Z, Z, Z

    for idx, member in enumerate(family):
        new_thread = Thread(idx + 1)
        new_thread.chord = family_chord
        new_thread.start(global_beat)
        member.set_braid_thread(new_thread)

    global_beat.trigger(update_all_patterns_3rd, 1, True)
    global_beat.start()
    play()


# if __name__ == "__main__":
#     # family_data = sys.argv[1]
#     family_data = "sch_family.csv"
#     run_sonification(family_data)
