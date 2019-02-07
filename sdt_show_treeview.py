from tkinter.ttk import Treeview


class SDTShowTreeview(Treeview):
    def __init__(self, master=None, sdt=None, set_cnt=1):
        Treeview.__init__(self, master, columns=("Red", "Green", "Blue"))
        self.sdt = sdt

        # Initialize Variables
        self.set_cnt = set_cnt
        self.set_iids = []  # Stores set iids within self

        self._init_treeview()

        # Bind method that prevents users from resizing the set
        # instruction columns
        self.bind("<Button-1>", self._block_column_resize)

    def populate_set_instructions(self, individual_show=None):
        if(individual_show is not None):
            for i in range(self.set_cnt):
                self.item(self.set_iids[i],
                          values=individual_show.set_instructions[i])

    def _block_column_resize(self, event):
        if(self.identify_region(event.x, event.y) == "separator"):
            return "break"

    def _init_sets(self):
        for i in range(self.set_cnt):
            self.set_iids.append(self.insert(
                parent="", index="end", text="{}".format(i + 1), open=False))

    def _init_treeview(self):
        self.column("#0", anchor="center", minwidth=50,
                    stretch=False, width=50)
        self.column("Red", anchor="center", minwidth=50,
                    stretch=True, width=50)
        self.column("Green", anchor="center", minwidth=50,
                    stretch=True, width=50)
        self.column("Blue", anchor="center", minwidth=50,
                    stretch=True, width=50)

        self.heading("#0", anchor="center", text="Set #")
        self.heading("Red", anchor="center", text="Red")
        self.heading("Green", anchor="center", text="Green")
        self.heading("Blue", anchor="center", text="Blue")

        self._init_sets()
