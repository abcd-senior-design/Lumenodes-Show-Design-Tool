from functools import partial
from sdt_ops_frame import SDTOpsFrame
from tkinter.ttk import Button


class SDTShowOps(SDTOpsFrame):
    def __init__(self, master=None):
        SDTOpsFrame.__init__(self, master, text="Show Operations")
        self._init_ops()

    def add_show(self):
        str = "Add Show"
        self.master.status_update(str)

    def remove_show(self):
        str = "Remove Show"
        self.master.status_update(str)

    def _init_ops(self):
        # Individual Show Operations
        self.add_show_button = Button(
            self, text="Add", command=partial(self.add_show))
        self._add(self.add_show_button)

        self.remove_show_button = Button(
            self, text="Remove", command=partial(self.remove_show))
        self._add(self.remove_show_button)
