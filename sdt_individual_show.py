# This is purely for being able to distinguish that the shows are actually
# updating via the new method (TODO: Remove on future commit)
from random import randint


class SDTIndividualShow:
    def __init__(self, master=None, sdt=None, set_cnt=1):
        self.master = master
        self.sdt = sdt

        # Initialize Variables
        self.set_cnt = set_cnt
        self.set_instructions = []

        self._init_show()

    def add_set_instruction(self):
        # Tuple Representing R, G, and B values respectively
        r = randint(0, 255)
        g = randint(0, 255)
        b = randint(0, 255)
        set_instruction = (r, g, b)
        self.set_instructions.append(set_instruction)

    def _init_show(self):
        for i in range(self.set_cnt):
            self.add_set_instruction()
