from tkinter.ttk import Treeview


class SDTAssignTreeview(Treeview):
    def __init__(self, master=None, sdt=None):
        Treeview.__init__(self, master)
        self.sdt = sdt

        # Initialize Variables
        self.pack_cnt = 0
        self.pack_iids = []  # Stores pack iids within self

        self._init_treeview()

        # Bind method that prevents users from resizing the pack info columns
        self.bind("<Button-1>", self._block_column_resize)

    def populate_pack_info_list(self, pack_strs):
        for i in range(self.pack_cnt):
            self.item(self.pack_iids[i], text=pack_strs[i])

    def reconfigure_pack_cnt(self, new_pack_cnt):
        self._adjust_pack_cnt(new_pack_cnt)

    def _add_pack_id(self):
        new_pack_iid = self.insert(parent="",
                                   index="end",
                                   open=False)
        self.pack_iids.append(new_pack_iid)

    def _adjust_pack_cnt(self, new_pack_cnt):
        diff = new_pack_cnt - self.pack_cnt
        self.pack_cnt = new_pack_cnt
        if(diff > 0):
            for i in range(diff):
                self._add_pack_id()
        elif(diff < 0):
            for i in range(-diff):
                tmp_pack_iid = self.pack_iids.pop()
                self.delete(tmp_pack_iid)

    def _block_column_resize(self, event):
        if(self.identify_region(event.x, event.y) == "separator"):
            return "break"

    def _init_treeview(self):
        self.column("#0", anchor="center", minwidth=40,
                    stretch=True, width=40)

        self.heading("#0", anchor="center", text="Pack")
