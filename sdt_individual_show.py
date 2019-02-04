from tkinter.ttk import Frame, Scrollbar, Treeview


class SDTIndividualShow(Frame):
    def __init__(self, master=None, set_cnt=1):
        Frame.__init__(self, master)
        self.master = master

        # Initialize Variables
        self.set_cnt = set_cnt
        self.set_instrs = []

        self._init_show()

        # Bind method that prevents users from resizing the set
        # instruction columns
        self.bind("<Button-1>", self._block_column_resize)

    def add_set_instr(self):
        # Tuple Representing R, G, and B values respectively
        set_instr = (0, 0, 0)
        self.set_instrs.append(set_instr)
        self.treeview.insert(parent="", index="end",
                             text="{}".format(len(self.set_instrs)),
                             open=False, values=set_instr)

    def _attach_scrollbar(self):
        self.scrollbar.configure(command=self.treeview.yview)
        self.treeview.configure(yscrollcommand=self.scrollbar.set)

    def _block_column_resize(self, event):
        if(self.identify_region(event.x, event.y) == "separator"):
            return "break"

    def _init_scrollbar(self):
        self.scrollbar = Scrollbar(master=self)
        self.scrollbar.grid(in_=self, row=0, column=1, sticky="ns")

    def _init_show(self):
        self._init_treeview()
        self._init_scrollbar()
        self._attach_scrollbar()
        for i in range(self.set_cnt):
            self.add_set_instr()

        self.grid_columnconfigure(index=0, weight=1)
        self.grid_rowconfigure(index=0, weight=1)

    def _init_treeview(self):
        self.treeview = Treeview(master=self, columns=("Red", "Green", "Blue"))

        self.treeview.column("#0", anchor="center", minwidth=50,
                             stretch=False, width=50)
        self.treeview.column("Red", anchor="center", minwidth=50,
                             stretch=True, width=50)
        self.treeview.column("Green", anchor="center", minwidth=50,
                             stretch=True, width=50)
        self.treeview.column("Blue", anchor="center", minwidth=50,
                             stretch=True, width=50)

        self.treeview.heading("#0", anchor="center", text="Set #")
        self.treeview.heading("Red", anchor="center", text="Red")
        self.treeview.heading("Green", anchor="center", text="Green")
        self.treeview.heading("Blue", anchor="center", text="Blue")

        self.treeview.grid(in_=self, row=0, column=0, sticky="nswe")
