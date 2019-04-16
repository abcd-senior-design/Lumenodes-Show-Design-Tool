from sdt_bounds import MAX_PACK_CNT
from sdt_pack_id_prompt import SDTPackIDPrompt
from sdt_pack_info import SDTPackInfo
from sdt_pack_treeview import SDTPackTreeview
from tkinter import messagebox
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
        if(self.pack_treeview.pack_cnt < MAX_PACK_CNT):
            self.pack_id_prompt = SDTPackIDPrompt(master=self,
                                                  sdt=self,
                                                  command=self._add_pack_id)
        else:
            messagebox.showerror(
                "Error",
                "Maximum number of {} Pack IDs reached!".format(MAX_PACK_CNT),
                parent=self.sdt)

    def alias_pack_id(self):
        return True

    def assign_pack_id(self):
        return True

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

        self.pack_treeview.reconfigure_pack_cnt(self.pack_cnt)

        self._update_pack_treeview()
        self._update_program_button()

    def remove_pack_id(self):
        success = False
        removed_pack_id = None

        if(self.pack_treeview.pack_cnt > 0):
            success = True
            self.pack_cnt -= 1
            pack_idx = self._get_current_pack_idx()

            removed_pack_info = self.pack_info_list.pop(pack_idx)
            removed_pack_id = removed_pack_info.get_id_str()

            self.pack_treeview.reconfigure_pack_cnt(self.pack_cnt)
            self._update_pack_treeview()
            self._update_program_button()
        else:
            messagebox.showerror(
                "Error",
                "No more Pack IDs to remove!",
                parent=self.sdt)
        return success, removed_pack_id

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

    def _extract_id_num(self, new_pack_id):
        try:
            return int(new_pack_id.replace(":", ""), 16)
        except:
            return -1

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

    def _update_pack_treeview(self):
        self.pack_treeview.populate_pack_info_list(self.pack_info_list)

    def _update_program_button(self):
        if(self.pack_cnt > 0):
            self.program_button.configure(state="normal")
        else:
            self.program_button.configure(state="disabled")
