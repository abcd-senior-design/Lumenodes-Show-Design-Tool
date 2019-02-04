# This is purely for being able to distinguish that the shows are actually
# updating via the new method (TODO: Remove on future commit)
from random import randint


class SDTIndividualShow:
    def __init__(self, master=None, set_cnt=1):
        self.master = master

        # Initialize Variables
        self.set_cnt = set_cnt
        self.set_instrs = []

        self._init_show()

    def add_set_instr(self):
        # Tuple Representing R, G, and B values respectively
        r = randint(0, 255)
        g = randint(0, 255)
        b = randint(0, 255)
        set_instr = (r, g, b)
        self.set_instrs.append(set_instr)

    def _init_show(self):
        for i in range(self.set_cnt):
            self.add_set_instr()
