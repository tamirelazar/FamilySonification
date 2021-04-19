import time


class SonicFamilyTree:

    # calendar
    # list of persons
    # music constants
    parser = None
    midi = None
    family = {}

    def __init__(self, parser, midi):
        self.parser = parser
        self.midi = midi
