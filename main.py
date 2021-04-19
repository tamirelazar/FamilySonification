# import time
# import pandas as pd

# from utils import FamilyParser
from braid import *
# from SonicFamilyTree import SonicFamilyTree

START_YEAR = 1990
END_YEAR = 2021


# # initialize the midi tool
# # midi = MidiTool()
# parser = FamilyParser("demo_family.csv")
# # tree = SonicFamilyTree(parser, midi)
#
# queen = next(parser)
# philip = next(parser)
#
# ### Queen Elizabeth II ###
# queen_bday = queen["Birth"]
# queen_birthday_idx = pd.date_range(queen_bday, "1960-01-01", freq=pd.DateOffset(years=1))
# queen_b = pd.Series("Birthday", index=queen_birthday_idx)
# queen_b[queen_bday] = "Birth"
# queen_b = pd.DataFrame({"Queen": queen_b})
#
# ### Prince Philip ###
# philip_bday = philip["Birth"]
# philip_birthday_idx = pd.date_range(philip_bday, "1960-01-01", freq=pd.DateOffset(years=1))
# philip_b = pd.Series("Birthday", index=philip_birthday_idx)
# philip_b[philip_bday] = "Birth"
# philip_b = pd.DataFrame({"Philip": philip_b})
#
# #print(pd.concat([queen_b, philip_b], axis=1))
#
# tempo(120)                  # set the universal tempo
#
#
#
# births = Thread(3)
# births.chord = E3, DOM
# births.pattern = 0, 0, 0, 0
# births.start()
#
# # drums = Thread(10)              # channel 10 is ,MIDI for drums
#
# # drums.pattern = [([K, H], [K, K]), (K, O)], (H, [H, K]), (S, [S, (O, K), 0, g(S)]), [[H, H], ([H, H], O, [g(S), g(S), g(S), g(S)])]         # K, S, H, O are built-in aliases for 36, 38, 42, 46
# # drums.start(births)
#
#
# def validate_birth():
#     # if validate_birth.curr_year >= 1921: # manually add philip birth in oct 1921
#     #     birth.pattern.add([0, 0, 2, 0])
#     # if validate_birth.curr_year >= 1926: # manually add queen birth in apr 1926
#     #     birth.pattern.add([0, 5, 0, 0])
#     def charles_birth():
#         if validate_birth.curr_year == 1949:
#             # birth.pattern.add([0, 0, 0, 7])
#             midiout.send_message([0x92, 60, 112])
#             time.sleep(0.25)
#             midiout.send_message([0x92, 60, 112])
#         else:
#             midiout.send_message([0x90, 60, 112])
#     if validate_birth.curr_year == 1948: # manually add charles birth in nov 1948
#         births.pattern.add([0, 0, 0, 7])
#     if validate_birth.curr_year == 1949:
#         birth.pattern.add([0, 0, 0, 7])
#         births.pattern = Z, Z, 0, 0
#     if validate_birth.curr_year == 1950: # manually add anne birth in aug 1950
#         births.pattern = [0, 0, [0, 4], 0]
#     if validate_birth.curr_year == 1951:
#         birth.pattern = [0, 5, [2, 4], 7]
#         validate_birth.curr_year += 6
#         births.pattern = Z, Z, 0, 0
#     if validate_birth.curr_year == 1960: # manually add andrew birth in feb 1960
#         births.pattern = [9, 0, [0, 0], 0]
#     if validate_birth.curr_year == 1961:
#         birth.pattern = [9, 5, [2, 4], 7]
#         births.pattern = Z, Z, 0, 0
#         validate_birth.curr_year += 1
#     if validate_birth.curr_year == 1964: # manually add edward birth in mar 1964
#         birth.pattern = [[9, 10], 5, [2, 4], 7]
#     validate_birth.curr_year += 1
#
#
# validate_birth.curr_year = 1945
#
#
#
#
# birth = Thread(1)
# birth.chord = E3, DOM
# birth.pattern = 0, 5, 2, 0
# birth.start(births)
# birth.trigger(validate_birth, 1, True)
#
#
# def validate_marriage():
#     if validate_marriage.curr_year == 1947: # manually add philip birth in oct 1921
#         marriage.pattern.add([0, 0, 0, [[5, 2], [0, 0]]])
#     if validate_marriage.curr_year > 1947:
#         if validate_marriage.curr_year % 2 == 0:
#             marriage.pattern = 0, Z, 0, [[2, 5], [Z, 0]]
#         else:
#             marriage.pattern = 0, 0, 0, [[5, 2], [Z, 0]]
#         # marriage.pattern = 0, 0, 0, Z
#     if validate_marriage.curr_year == 1950: # manually add anne birth in aug 1950
#         validate_marriage.curr_year += 6
#     if validate_marriage.curr_year == 1960: # manually add andrew birth in feb 1960
#         validate_marriage.curr_year += 1
#     validate_marriage.curr_year += 1
#
#
# validate_marriage.curr_year = 1945
#
# marriage = Thread(2)
# marriage.chord = E3, DOM
# marriage.pattern = 0, 0, 0, 0
# marriage.start(births)
# marriage.trigger(validate_marriage, 1, True)
#
# play()

# plan: create beat thread which sends 4 quarters to a quarter calculation function

def build_quarter(year, q):
    """
    gets the number of quarter to calculate and the current year
    :param q:
    :return:
    """
    ret = []
    for i in range(q):
        ret.append(q)
    if q == 3:
        sub_beat.play(1)
    if q == 4:
        subsub_beat.play(1)
    return ret


tempo(120)  # global
year = START_YEAR
def year_inc():
    global year
    year += 1
    if year == 2022:
        global_beat.stop()

global_beat = Thread(1)
sub_beat = Thread(2)
subsub_beat = Thread(3)
sub_beat.chord = E3, DOM
subsub_beat.chord = E3, DOM
global_beat.chord = E3, DOM
global_beat.pattern = [build_quarter(year, 1), build_quarter(year, 2), build_quarter(year, 3), build_quarter(year, 4)]
global_beat.trigger(year_inc, 1, True)
global_beat.start()
sub_beat.start(global_beat)
subsub_beat.start(global_beat)


play()