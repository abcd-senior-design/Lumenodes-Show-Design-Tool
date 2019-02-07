from functools import partial
from sdt_ops_frame import SDTOpsFrame
from tkinter.ttk import Button


class SDTShowOps(SDTOpsFrame):
    def __init__(self, master=None, sdt=None):
        SDTOpsFrame.__init__(self, master=master, sdt=sdt,
                             text="Show Operations")

        self._init_ops()

    def add_show(self):
        self._sdt_status_update("Add Show")

    def remove_show(self):
        self._sdt_status_update("Remove Show")

    def _init_ops(self):
        # Individual Show Operations
        self.add_show_button = Button(
            self, text="Add", command=partial(self.add_show))
        self._add(self.add_show_button)

        self.remove_show_button = Button(
            self, text="Remove", command=partial(self.remove_show))
        self._add(self.remove_show_button)
