import time
import pandas as pd
import rtmidi as rtmidi

from utils import MidiTool, FamilyParser
from braid import *
from SonicFamilyTree import SonicFamilyTree


# initialize the midi tool
# midi = MidiTool()
parser = FamilyParser("demo_family.csv")
tree = SonicFamilyTree(parser, midi)


# demo low-level code

# creating separate midiout
midiout = rtmidi.MidiOut()
available_ports = midiout.get_ports()

# here we're printing the ports to check that we see the one that loopMidi created.
# In the list we should see a port called "loopMIDI port".
print("Available Ports:")
print(available_ports)

# Attempt to open the port
if available_ports:
    midiout.open_port(0)
    print("Port opened: " + available_ports[0])
else:
    midiout.open_virtual_port("My virtual output")

queen = next(parser)
philip = next(parser)

### Queen Elizabeth II ###
queen_bday = queen["Birth"]
queen_birthday_idx = pd.date_range(queen_bday, "1960-01-01", freq=pd.DateOffset(years=1))
queen_b = pd.Series("Birthday", index=queen_birthday_idx)
queen_b[queen_bday] = "Birth"
queen_b = pd.DataFrame({"Queen": queen_b})

### Prince Philip ###
philip_bday = philip["Birth"]
philip_birthday_idx = pd.date_range(philip_bday, "1960-01-01", freq=pd.DateOffset(years=1))
philip_b = pd.Series("Birthday", index=philip_birthday_idx)
philip_b[philip_bday] = "Birth"
philip_b = pd.DataFrame({"Philip": philip_b})

#print(pd.concat([queen_b, philip_b], axis=1))

tempo(120)                  # set the universal tempo



births = Thread(3)
births.chord = E3, DOM
births.pattern = 0, 0, 0, 0
births.start()

drums = Thread(10)              # channel 10 is ,MIDI for drums

drums.pattern = [([K, H], [K, K]), (K, O)], (H, [H, K]), (S, [S, (O, K), 0, g(S)]), [[H, H], ([H, H], O, [g(S), g(S), g(S), g(S)])]         # K, S, H, O are built-in aliases for 36, 38, 42, 46
drums.start(births)


def validate_birth():
    # if validate_birth.curr_year >= 1921: # manually add philip birth in oct 1921
    #     birth.pattern.add([0, 0, 2, 0])
    # if validate_birth.curr_year >= 1926: # manually add queen birth in apr 1926
    #     birth.pattern.add([0, 5, 0, 0])
    def charles_birth():
        if validate_birth.curr_year == 1949:
            # birth.pattern.add([0, 0, 0, 7])
            midiout.send_message([0x92, 60, 112])
            time.sleep(0.25)
            midiout.send_message([0x92, 60, 112])
        else:
            midiout.send_message([0x90, 60, 112])
    if validate_birth.curr_year == 1948: # manually add charles birth in nov 1948
        births.pattern.add([0, 0, 0, 7])
    if validate_birth.curr_year == 1949:
        birth.pattern.add([0, 0, 0, 7])
        births.pattern = Z, Z, 0, 0
    if validate_birth.curr_year == 1950: # manually add anne birth in aug 1950
        births.pattern = [0, 0, [0, 4], 0]
    if validate_birth.curr_year == 1951:
        birth.pattern = [0, 5, [2, 4], 7]
        validate_birth.curr_year += 6
        births.pattern = Z, Z, 0, 0
    if validate_birth.curr_year == 1960: # manually add andrew birth in feb 1960
        births.pattern = [9, 0, [0, 0], 0]
    if validate_birth.curr_year == 1961:
        birth.pattern = [9, 5, [2, 4], 7]
        births.pattern = Z, Z, 0, 0
        validate_birth.curr_year += 1
    if validate_birth.curr_year == 1964: # manually add edward birth in mar 1964
        birth.pattern = [[9, 10], 5, [2, 4], 7]
    validate_birth.curr_year += 1


validate_birth.curr_year = 1945




birth = Thread(1)
birth.chord = E3, DOM
birth.pattern = 0, 5, 2, 0
birth.start(births)
birth.trigger(validate_birth, 1, True)


def validate_marriage():
    if validate_marriage.curr_year == 1947: # manually add philip birth in oct 1921
        marriage.pattern.add([0, 0, 0, [[5, 2], [0, 0]]])
    if validate_marriage.curr_year > 1947:
        if validate_marriage.curr_year % 2 == 0:
            marriage.pattern = 0, Z, 0, [[2, 5], [Z, 0]]
        else:
            marriage.pattern = 0, 0, 0, [[5, 2], [Z, 0]]
        # marriage.pattern = 0, 0, 0, Z
    if validate_marriage.curr_year == 1950: # manually add anne birth in aug 1950
        validate_marriage.curr_year += 6
    if validate_marriage.curr_year == 1960: # manually add andrew birth in feb 1960
        validate_marriage.curr_year += 1
    validate_marriage.curr_year += 1


validate_marriage.curr_year = 1945

marriage = Thread(2)
marriage.chord = E3, DOM
marriage.pattern = 0, 0, 0, 0
marriage.start(births)
marriage.trigger(validate_marriage, 1, True)

play()


# go over each line in turn
# validating dates to be after parent's meeting
# creating event objects from each item, pouring them all into a list
# sorting the events using a custom comparator
# playing the events, by going over the sorted list in parallel to the full calendar (monthly). If the month has no
#      events, sleep for a moment. At the end of each year, sleep for a measure as well (to reach 16 bars a year).
#      If a month has events, play them evenly spaced/realistically spaced (tbd), wait and continue.

# That doesn't make much sense. Just write a calendar and put the events into it, combining the two lists.

# What that means for events
# I need an event object, which will contain date information, a name and a type (birth, marriage).
# Does this means I need people objects, to connect to it? maybe

# Music
# As a start, I think I'll focus on a family my size, and so can choose a pentatonic scale to assign.
# To separate event types, different instruments and volumes will be utilized? yes, for now

#
# midi.send("note_on", "G_3", 112)
# time.sleep(0.5)
# midi.send("note_off", "G_3", 0)

# workframe for braid
# 1 create a thread for each channel, connected to different instruments which represent event types ("birthday
#   channel" etc)
# 2 at the beginning of each year (a 12/4 measure), check each feed using trigger, read ahead to see what should be
#   added to each event feed (no substraction, as a statement - but maybe change of sound)
### notes ###
# can build a tone:name dictionary to more easily change the patterns