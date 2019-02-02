from functools import partial
from sdt_ops_frame import SDTOpsFrame
from tkinter.ttk import Button


class SDTInstrOps(SDTOpsFrame):
    def __init__(self, master=None):
        SDTOpsFrame.__init__(self, master, text="Set Instruction Operations")
        self._init_ops()

    def clear_set_instr(self):
        str = "Clear Set Instruction"
        self.master.status_update(str)

    def edit_set_instr(self):
        str = "Edit Set Instruction"
        self.master.status_update(str)

    def _init_ops(self):
        # Set Instruction Operations
        self.edit_set_instr_button = Button(
            self, text="Edit", command=partial(self.edit_set_instr))
        self._add(self.edit_set_instr_button)

        self.clear_set_instr_button = Button(
            self, text="Clear", command=partial(self.clear_set_instr))
        self._add(self.clear_set_instr_button)
