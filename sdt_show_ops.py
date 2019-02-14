from functools import partial
from sdt_ops_frame import SDTOpsFrame
from tkinter.ttk import Button


class SDTShowOps(SDTOpsFrame):
    def __init__(self, master=None, sdt=None):
        SDTOpsFrame.__init__(self, master=master, sdt=sdt,
                             text="Show Operations")

        self._init_ops()

    def add_show(self):
        success = self.sdt.add_individual_show()
        if(success):
            self._sdt_status_update(
                "Added Show #{}".format(self.sdt.individual_show_cnt))

    def remove_show(self):
        old_show_cnt = self.sdt.individual_show_cnt
        success, removed_show = self.sdt.remove_individual_show()
        if(success and old_show_cnt != self.sdt.individual_show_cnt):
            if(old_show_cnt != removed_show):
                self._sdt_status_update(
                    "Removed Show #{}. ".format(removed_show) +
                    "Other shows shifted to fill the hole")
            else:
                self._sdt_status_update(
                    "Removed Show #{}".format(removed_show))
        elif(success and old_show_cnt == self.sdt.individual_show_cnt):
            self._sdt_status_update(
                "Cleared Show #{}".format(self.sdt.individual_show_cnt))

    def _init_ops(self):
        # Individual Show Operations
        self.add_show_button = Button(
            self, text="Add", command=partial(self.add_show))
        self._add(self.add_show_button)

        self.remove_show_button = Button(
            self, text="Remove", command=partial(self.remove_show))
        self._add(self.remove_show_button)
