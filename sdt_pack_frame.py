from sdt_pack_treeview import SDTPackTreeview
from tkinter.ttk import Button, Frame, Scrollbar


class SDTPackFrame(Frame):
    def __init__(self, master=None, sdt=None):
        Frame.__init__(self, master)
        self.sdt = sdt

        # Initialize Variables
        self.pack_cnt = 0
        self.pack_info_list = []  # Stores SDTPackInfo objects

        self._init_frame()

    def add_pack_id(self):
        return True

    def alias_pack_id(self):
        return True

    def assign_pack_id(self):
        return True

    def remove_pack_id(self):
        return True

    def _init_frame(self):
        self.grid_columnconfigure(index=0, weight=1)
        self.grid_rowconfigure(index=1, weight=1)

        # Program Button
        self.program_button = Button(master=self,
                                     state="disabled",
                                     text="Program")
        self.program_button.grid(in_=self, column=0, row=0, sticky="")

        # Pack Treeview
        self.pack_treeview = SDTPackTreeview(master=self, sdt=self.sdt)
        self.pack_treeview.grid(in_=self, column=0, row=1, sticky="nswe")

        # Pack Scrollbar
        self.pack_scrollbar = Scrollbar(master=self,
                                        command=self.pack_treeview.yview)
        self.pack_treeview.configure(yscrollcommand=self.pack_scrollbar.set)
        self.pack_scrollbar.grid(in_=self, column=1, row=1, sticky="ns")
