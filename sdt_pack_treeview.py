from tkinter.ttk import Treeview


class SDTPackTreeview(Treeview):
    def __init__(self, master=None, sdt=None):
        Treeview.__init__(self, master, columns=())
        self.sdt = sdt

        # Initialize Variables
        self.pack_cnt = 0
        self.pack_iids = []  # Stores pack info iids within self

        self._init_treeview()

        # Bind method that prevents users from resizing the pack info columns
        self.bind("<Button-1>", self._block_column_resize)

    def _block_column_resize(self, event):
        if(self.identify_region(event.x, event.y) == "separator"):
            return "break"

    def _init_treeview(self):
        self.column("#0", anchor="center", minwidth=40,
                    stretch=True, width=40)

        self.heading("#0", anchor="center", text="Pack ID")
