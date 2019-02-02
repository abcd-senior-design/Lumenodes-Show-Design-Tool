from functools import partial
from sdt_ops_frame import SDTOpsFrame
from tkinter.ttk import Button


class SDTFileOps(SDTOpsFrame):
    def __init__(self, master=None):
        SDTOpsFrame.__init__(self, master, text="File Operations")
        self._init_ops()

    def create_new_file(self):
        str = "Create New File"
        self.master.status_update(str)

    def open_file(self):
        str = "Open File"
        self.master.status_update(str)

    def save_file(self):
        str = "Save File"
        self.master.status_update(str)

    def _init_ops(self):
        # Global Show (File) Operations
        self.new_file_button = Button(
            self, text="New", command=partial(self.create_new_file))
        self._add(self.new_file_button)

        self.open_file_button = Button(
            self, text="Open", command=partial(self.open_file))
        self._add(self.open_file_button)

        self.save_file_button = Button(
            self, text="Save", command=partial(self.save_file))
        self._add(self.save_file_button)
