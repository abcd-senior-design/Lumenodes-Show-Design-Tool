from functools import partial
from sdt_ops_frame import SDTOpsFrame
from tkinter.ttk import Button


class SDTInstructionOps(SDTOpsFrame):
    def __init__(self, master=None, sdt=None):
        SDTOpsFrame.__init__(self, master=master, sdt=sdt,
                             text="Set Instruction Operations")

        self._init_ops()

    def clear_set_instruction(self):
        show_num, set_num = self.sdt.clear_set_instruction()
        self._sdt_status_update(
            "Cleared Set Instruction #{} in Show #{}".format(
                set_num, show_num))

    def edit_set_instruction(self):
        success, show_num, set_num = self.sdt.edit_set_instruction()
        if(success):
            self._sdt_status_update(
                "Edited Set Instruction #{} in Show #{}".format(
                    set_num, show_num))

    def _init_ops(self):
        # Set Instruction Operations
        self.edit_set_instruction_button = Button(
            self, text="Edit", command=partial(self.edit_set_instruction))
        self._add(self.edit_set_instruction_button)

        self.clear_set_instruction_button = Button(
            self, text="Clear", command=partial(self.clear_set_instruction))
        self._add(self.clear_set_instruction_button)
