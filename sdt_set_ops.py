from functools import partial
from sdt_ops_frame import SDTOpsFrame
from tkinter.ttk import Button


class SDTSetOps(SDTOpsFrame):
    def __init__(self, master=None, sdt=None):
        SDTOpsFrame.__init__(self, master=master, sdt=sdt,
                             text="Set Operations")

        self._init_ops()

    def add_set(self):
        self._sdt_status_update("Add Set")

    def remove_set(self):
        self._sdt_status_update("Remove Set")

    def _init_ops(self):
        # Set Operations
        self.add_set_button = Button(
            self, text="Add", command=partial(self.add_set))
        self._add(self.add_set_button)

        self.remove_set_button = Button(
            self, text="Remove", command=partial(self.remove_set))
        self._add(self.remove_set_button)
