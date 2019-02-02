from functools import partial
from sdt_ops_frame import SDTOpsFrame
from tkinter.ttk import Button


class SDTPackOps(SDTOpsFrame):
    def __init__(self, master=None):
        SDTOpsFrame.__init__(self, master, text="Pack Operations")
        self._init_ops()

    def add_pack_id(self):
        str = "Add Pack ID"
        self.master.status_update(str)

    def alias_pack_id(self):
        str = "Alias Pack ID"
        self.master.status_update(str)

    def assign_pack_id(self):
        str = "Assign Pack ID"
        self.master.status_update(str)

    def remove_pack_id(self):
        str = "Remove Pack ID"
        self.master.status_update(str)

    def _init_ops(self):
            # Pack Operations
        self.add_pack_id_button = Button(
            self, text="Add Pack ID", command=partial(self.add_pack_id))
        self._add(self.add_pack_id_button)

        self.remove_pack_id_button = Button(
            self, text="Remove Pack ID", command=partial(self.remove_pack_id))
        self._add(self.remove_pack_id_button)

        self.alias_pack_id_button = Button(
            self, text="Alias Pack ID", command=partial(self.alias_pack_id))
        self._add(self.alias_pack_id_button)

        self.assign_pack_id_button = Button(
            self, text="Assign Pack ID", command=partial(self.assign_pack_id))
        self._add(self.assign_pack_id_button)
