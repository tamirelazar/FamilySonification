# family_sonification

# communication with ableton
To communicate with Ableton, you have to:
    1) open a virtual port
    2) connect Ableton to that port
    3) get a MidiOut device from rtmidi
    4) locate your port, and open it inside your MidiOut device
    5) use your MidiOut's send_message() to get midi signal to virtual port
    
# 1 - Open Virtual Port
Can be done on mac using Audio Midi Setup, a builtin tool. 
Just activate the IAC Driver tool using the "device online" checkbox.

# 2 - Connect Ableton
Switch to the IAC under "Midi From" tag, on the lower third part of a Midi Channel.

# 3, 4, 5 - Set up MidiOut device, connect to port and send MIDI
Here is some example code I found online:

```python
import time
import rtmidi

midiout = rtmidi.MidiOut()
available_ports = midiout.get_ports()

# here we're printing the ports to check that we see the one that loopMidi created.
# In the list we should see a port called "loopMIDI port".
print(available_ports)

# Attempt to open the port
if available_ports:
    midiout.open_port(0)
else:
    midiout.open_virtual_port("My virtual output")


note_on = [0x90, 60, 112]
note_off = [0x80, 60, 0]
midiout.send_message(note_on)


del midiout
```

# MIDI messages
In all MIDI messages, you send three hex numbers: status (message type) and two data bits dependant on the first.
This is all in hex (preceded by 0x), but can be done in ascii as well.

Note On: 0x9# (# is the Ableton channel to send to, minus 1, because count starts from 0 here)
    2nd Bit: Note to play   3rd Bit: Velocity
    
Note On: 0x8# (# is the Ableton channel to send to, minus 1, because count starts from 0 here)
    2nd Bit: Note to play   3rd Bit: Velocity
    
# Some Hands-On Examples
I found the MIDI sequence to play the following measure:
![alt-text](http://www.music-software-development.com/images/Midi-example-1.jpg)

Which is the following.

```python
# t=0 : 0x90 - 0x40 - 0x40 (Start of E3 note, pitch = 64)
# t=0 : 0x90 - 0x43 - 0x40 (Start of G3 note, pitch= 67)
midiout.send_message([0x90, 0x40, 0x40])
midiout.send_message([0x90, 0x43, 0x40])
time.sleep(1)
# t=1 : 0x80 - 0x43 - 0x00 (End of G3 note, pitch=67)
# t=1 : 0x90 - 0x45 - 0x40 (Start of A3 note, pitch=69)
midiout.send_message([0x80, 0x43, 0x00])
midiout.send_message([0x90, 0x45, 0x40])
time.sleep(1)
# t=2 : 0x80 - 0x45 - 0x00 (End of A3 note, pitch=69)
# t=2 : 0x80 - 0x40 - 0x00 (End of E3 note, pitch=64)
# t=2 : 0x90 - 0x3C - 0x40 (Start of C3 note, pitch = 60)
# t=2 : 0x90 - 0x47 - 0x40 (Start of B3 note, pitch= 71)
midiout.send_message([0x80, 0x45, 0x00])
midiout.send_message([0x80, 0x40, 0x00])
midiout.send_message([0x90, 0x3C, 0x40])
midiout.send_message([0x90, 0x47, 0x40])
time.sleep(1)
# t=3 : 0x80 - 0x47 - 0x00 (End of B3 note, pitch= 71)
# t=3 : 0x90 - 0x48 - 0x40 (Start of C4 note, pitch= 72)
midiout.send_message([0x80, 0x47, 0x00])
midiout.send_message([0x90, 0x48, 0x40])
time.sleep(1)
# t=4 : 0x80 - 0x48 - 0x00 (End of C4 note, pitch= 72)
# t=4 : 0x80 - 0x3C - 0x40 (End of C3 note, pitch = 60)
midiout.send_message([0x80, 0x48, 0x00])
midiout.send_message([0x80, 0x3C, 0x40])
```

when t is time in seconds.