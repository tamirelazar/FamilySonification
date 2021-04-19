import time
import csv
import rtmidi

# class MidiTool:
#     midiout = None
#
#     def __init__(self):
#         self.midiout = rtmidi.MidiOut()
#         available_ports = self.midiout.get_ports()
#
#         # here we're printing the ports to check that we see the one that loopMidi created.
#         # In the list we should see a port called "loopMIDI port".
#         print("Available Ports:")
#         print(available_ports)
#
#         # Attempt to open the port
#         if available_ports:
#             self.midiout.open_port(0)
#             print("Port opened: " + available_ports[0])
#         else:
#             self.midiout.open_virtual_port("My virtual output")
#
#     def note_value(self, note_string):
#         if isinstance(note_string, int):
#             return note_string
#         else:
#             return midi.NOTE_NAME_MAP_FLAT[note_string]
#
#     def send(self, status, data1, data2):
#         if status == "note_on":
#             tone = self.note_value(data1)
#             velocity = data2
#             self.midiout.send_message([NOTE_ON, tone, velocity])
#         elif status == "note_off":
#             tone = self.note_value(data1)
#             velocity = data2
#             self.midiout.send_message([NOTE_OFF, tone, velocity])
#
#     def __del__(self):
#         del self.midiout
#

class FamilyParser:
    family_data = None
    raw_csv = None

    def __init__(self, csv_file):
        self.raw_csv = open(csv_file, newline='', encoding='utf-8-sig')
        self.family_data = csv.DictReader(self.raw_csv)

    def __del__(self):
        self.raw_csv.close()

    def __next__(self):
        return next(self.family_data)

