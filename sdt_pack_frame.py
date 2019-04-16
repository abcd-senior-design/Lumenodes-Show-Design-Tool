from sdt_alias_entry import SDTAliasEntry
from sdt_bounds import MAX_PACK_CNT
from sdt_pack_id_prompt import SDTPackIDPrompt
from sdt_pack_info import SDTPackInfo
from sdt_pack_treeview import SDTPackTreeview
from sdt_show_assign_prompt import SDTShowAssignPrompt
from tkinter import messagebox
from tkinter.ttk import Button, Frame, Scrollbar


class SDTPackFrame(Frame):
    def __init__(self, master=None, sdt=None, show_cnt=1):
        Frame.__init__(self, master)
        self.sdt = sdt

        # Initialize Variables
        self.pack_cnt = 0
        self.pack_info_list = []  # Stores SDTPackInfo objects
        self.show_cnt = show_cnt

        self.alias_entry = None
        self.bind("<Configure>", self._move_alias_entry)

        self._init_frame()

    def add_individual_show(self):
        self.show_cnt += 1

    def add_pack_id(self):
        if(self.pack_treeview.pack_cnt < MAX_PACK_CNT):
            self.pack_id_prompt = SDTPackIDPrompt(master=self,
                                                  sdt=self,
                                                  command=self._add_pack_id)
        else:
            messagebox.showerror(
                "Error",
                "Maximum number of {} Pack IDs reached!".format(MAX_PACK_CNT),
                parent=self.sdt)

    def alias_pack_id(self, alias=None):
        if(self.alias_entry is not None):
            self._destroy_alias_entry()
        pack_idx = self._get_current_pack_idx()
        if(pack_idx >= 0):
            if(alias is None):
                alias = self._get_cell_contents(pack_idx, 1)
            self.alias_entry = SDTAliasEntry(
                master=self.pack_treeview,
                sdt=self.sdt,
                alias=alias,
                command=self.update_pack_alias,
                destroy_command=self._destroy_alias_entry)
            self._move_alias_entry(None)

        elif(self.pack_cnt == 0):
            messagebox.showerror(
                "Error",
                "No Pack IDs to alias!",
                parent=self.sdt)
        else:
            messagebox.showerror(
                "Error",
                "Please select Pack ID to alias!",
                parent=self.sdt)

    def assign_pack_id(self):
        if(self.pack_cnt == 0):
            messagebox.showerror(
                "Error",
                "No Pack IDs to assign!",
                parent=self.sdt)
        else:
            self.assign_prompt = SDTShowAssignPrompt(
                master=self,
                sdt=self.sdt,
                show_cnt=self.show_cnt,
                pack_info_list=self.pack_info_list,
                destroy_command=self._destroy_assign_prompt)

    def get_pack_info_list(self):
        pack_info_list = []

        for i in range(self.pack_cnt):
            pack_info = self.pack_info_list[i].get_pack_info()
            pack_info_list.append(pack_info)

        return pack_info_list

    def reconfigure_pack_list(self, new_pack_info_list):
        self.pack_cnt = 0
        self.pack_info_list = []
        for i in range(len(new_pack_info_list)):
            new_pack_id_num = self._extract_id_num(
                new_pack_info_list[i]["pack_id"])
            if(new_pack_id_num >= 0):
                if(not self._is_in_pack_info_list(new_pack_id_num)):
                    self._add_pack_info(new_pack_id_num)

                    new_pack_alias = new_pack_info_list[i]["pack_alias"]
                    if(type(new_pack_alias) is str and
                       new_pack_alias != "N/A"):
                        new_alias_symbol, new_alias_number = \
                            SDTAliasEntry.extract_alias(new_pack_alias)
                        self.pack_info_list[-1].set_pack_alias(
                            new_alias_symbol, new_alias_number)
                    new_pack_assignment = \
                        new_pack_info_list[i]["pack_assignment"]
                    if(new_pack_assignment <= 0 or
                       new_pack_assignment > self.show_cnt):
                        new_pack_assignment = 0
                    self.pack_info_list[-1].set_pack_assignment(
                        new_pack_assignment - 1)

        self.pack_treeview.reconfigure_pack_cnt(self.pack_cnt)

        self._update_pack_treeview()
        self._update_program_button()

    def reconfigure_show_cnt(self, new_show_cnt):
        self.show_cnt = new_show_cnt
        for pack_info in self.pack_info_list:
            if(pack_info.show_idx >= new_show_cnt):
                pack_info.set_pack_assignment(-1)
        self._update_pack_treeview()

    def remove_individual_show(self, removed_show_idx):
        self.show_cnt -= 1
        for pack_info in self.pack_info_list:
            if(pack_info.show_idx > removed_show_idx):
                pack_info.set_pack_assignment(pack_info.show_idx - 1)
            elif(pack_info.show_idx == removed_show_idx):
                pack_info.set_pack_assignment(-1)

        if(self.show_cnt <= 0):
            self.show_cnt = 1
        self._update_pack_treeview()

    def remove_pack_id(self):
        success = False
        removed_pack_id = None
        removed_pack_alias = None

        if(self.pack_treeview.pack_cnt > 0):
            success = True
            self.pack_cnt -= 1
            pack_idx = self._get_current_pack_idx()

            removed_pack_info = self.pack_info_list.pop(pack_idx)
            removed_pack_id = removed_pack_info.get_id_str()
            removed_pack_alias = removed_pack_info.get_alias_str()

            self.pack_treeview.reconfigure_pack_cnt(self.pack_cnt)
            self._update_pack_treeview()
            self._update_program_button()
        else:
            messagebox.showerror(
                "Error",
                "No more Pack IDs to remove!",
                parent=self.sdt)
        return success, removed_pack_id, removed_pack_alias

    def update_pack_alias(self):
        new_alias_symbol = self.alias_entry.alias_symbol.get()
        new_alias_number = self.alias_entry.alias_number.get()
        new_pack_alias = "%c%d" % (new_alias_symbol, new_alias_number)

        pack_alias_used = False
        for i in range(len(self.pack_info_list)):
            pack_info = self.pack_info_list[i]
            if(pack_info.get_alias_str() == new_pack_alias and
               i != self._get_current_pack_idx()):
                messagebox.showerror(
                    "Error",
                    "Pack ID {} already has Pack Alias {}".format(
                        pack_info.get_id_str(), new_pack_alias),
                    parent=self.sdt)
                pack_alias_used = True
                break

        if(not pack_alias_used):
            pack_idx = self._get_current_pack_idx()
            pack_info = self.pack_info_list[pack_idx]
            pack_info.set_pack_alias(new_alias_symbol, new_alias_number)

            self._update_pack_treeview()
            self._destroy_alias_entry()

            if(self.sdt is not None):
                self.sdt.status_update("Aliased Pack ID {} to {}".format(
                    pack_info.get_id_str(),
                    pack_info.get_alias_str()))
        else:
            self.alias_pack_id(alias=new_pack_alias)

    def _add_pack_id(self):
        new_pack_id = self.pack_id_prompt.get_pack_id()
        new_pack_id_str = self.pack_id_prompt.get_pack_id_str()
        self.pack_id_prompt.destroy()
        if(new_pack_id >= 0):
            if(not self._is_in_pack_info_list(new_pack_id)):
                self._add_pack_info(new_pack_id)

                self.pack_treeview.reconfigure_pack_cnt(self.pack_cnt)
                self._update_pack_treeview()
                self._update_program_button()

                if(self.sdt is not None):
                    self.sdt.status_update(
                        "Added Pack ID {}".format(new_pack_id_str))
            else:
                messagebox.showerror(
                    "Error",
                    "Pack ID {} already added!".format(new_pack_id_str),
                    parent=self.sdt
                )
        else:
            messagebox.showerror(
                "Error",
                "Pack ID {} is invalid!".format(new_pack_id_str),
                parent=self.sdt
            )

    def _add_pack_info(self, new_pack_id_num):
        self.pack_cnt += 1
        pack_info = SDTPackInfo(master=self, sdt=self.sdt,
                                pack_id=new_pack_id_num)
        self.pack_info_list.append(pack_info)

    def _destroy_alias_entry(self):
        if(self.alias_entry is not None):
            self.alias_entry.destroy()
            self.alias_entry = None

    def _destroy_assign_prompt(self):
        if(self.assign_prompt is not None):
            self._update_pack_treeview()
            self.assign_prompt.destroy()
            self.assign_prompt = None

    def _extract_id_num(self, new_pack_id):
        try:
            return int(new_pack_id.replace(":", ""), 16)
        except:
            return -1

    def _get_cell_bounds(self, pack_idx, column):
        pack_iid = self.pack_treeview.pack_iids[pack_idx]
        if(column == 0):
            return self.pack_treeview.bbox(pack_iid)
        else:
            return self.pack_treeview.bbox(pack_iid, column - 1)

    def _get_cell_contents(self, pack_idx, column):
        pack_iid = self.pack_treeview.pack_iids[pack_idx]
        if(column == 0):
            return self.pack_treeview.item(pack_iid, 'text')
        else:
            return self.pack_treeview.item(pack_iid, 'values')[column - 1]

    def _get_current_pack_idx(self):
        curr_pack_iid = self.pack_treeview.focus()
        curr_pack_idx = -1
        if(curr_pack_iid != ""):
            curr_pack_idx = self.pack_treeview.index(curr_pack_iid)
        return curr_pack_idx

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

    def _is_in_pack_info_list(self, pack_id_num):
        pack_id_nums = [pack_info.pack_id for pack_info in self.pack_info_list]
        for curr_num in pack_id_nums:
            if(curr_num == pack_id_num):
                return True
        return False

    def _move_alias_entry(self, event):
        if(self.alias_entry is not None):
            pack_idx = self._get_current_pack_idx()
            x, y, width, height = self._get_cell_bounds(pack_idx, 1)

            pady = height // 2
            self.alias_entry.place(anchor="w",
                                   width=width,
                                   x=x,
                                   y=(y + pady))
            self.alias_entry.focus()

    def _update_pack_treeview(self):
        self.pack_treeview.populate_pack_info_list(self.pack_info_list)

    def _update_program_button(self):
        if(self.pack_cnt > 0):
            self.program_button.configure(state="normal")
        else:
            self.program_button.configure(state="disabled")
