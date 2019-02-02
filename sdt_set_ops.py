from functools import partial
from sdt_ops_frame import SDTOpsFrame
from tkinter.ttk import Button


class SDTSetOps(SDTOpsFrame):
    def __init__(self, master=None):
        SDTOpsFrame.__init__(self, master, text="Set Operations")
        self._init_ops()

    def add_set(self):
        str = "Add Set"
        self.master.status_update(str)

    def remove_set(self):
        str = "Remove Set"
        self.master.status_update(str)

    def _init_ops(self):
        # Set Operations
        self.add_set_button = Button(
            self, text="Add", command=partial(self.add_set))
        self._add(self.add_set_button)

        self.remove_set_button = Button(
            self, text="Remove", command=partial(self.remove_set))
        self._add(self.remove_set_button)
