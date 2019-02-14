from functools import partial
from sdt_ops_frame import SDTOpsFrame
from tkinter.ttk import Button


class SDTSetOps(SDTOpsFrame):
    def __init__(self, master=None, sdt=None):
        SDTOpsFrame.__init__(self, master=master, sdt=sdt,
                             text="Set Operations")

        self._init_ops()

    def add_set(self):
        success = self.sdt.add_set()
        if(success):
            self._sdt_status_update(
                "Added Set #{}".format(self.sdt.set_cnt))

    def remove_set(self):
        success, removed_set = self.sdt.remove_set()
        if(success):
            if(removed_set != self.sdt.set_cnt + 1):
                self._sdt_status_update(
                    "Removed Set #{}. ".format(removed_set) +
                    "Other sets shifted to fill the hole")
            else:
                self._sdt_status_update("Removed Set #{}".format(removed_set))

    def _init_ops(self):
        # Set Operations
        self.add_set_button = Button(
            self, text="Add", command=partial(self.add_set))
        self._add(self.add_set_button)

        self.remove_set_button = Button(
            self, text="Remove", command=partial(self.remove_set))
        self._add(self.remove_set_button)
