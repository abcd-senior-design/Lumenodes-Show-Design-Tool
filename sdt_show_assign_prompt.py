from sdt_assign_treeview import SDTAssignTreeview
from sdt_show_spinbox import SDTShowSpinbox
from tkinter import BooleanVar, Toplevel
from tkinter.ttk import Button, Checkbutton, Label, Scrollbar


class SDTShowAssignPrompt(Toplevel):
    def __init__(self, master=None, sdt=None,
                 pack_info_list=[], show_cnt=1, destroy_command=None):
        Toplevel.__init__(self, master, pady=10)
        self.title("Assign Pack IDs")
        self.resizable(False, False)
        self.transient(self.master)  # Keeps prompt under same taskbar icon
        self.focus()  # Forces focus to be on this prompt
        # Grabs all events from other window, preventing interaction with
        # main window while the prompt is open
        self.grab_set()
        self.lift()  # Brings this window to the top of the window stack

        # Initialize Variables
        self.sdt = sdt
        self.pack_info_list = pack_info_list
        self.show_cnt = show_cnt
        self.use_aliases = BooleanVar()
        self.use_aliases.set(True)

        # Generate Assigned and Unassigned Lists of Pack IDs
        self.unassigned_pack_info_list = \
            [
                self.pack_info_list[i]
                for i in range(len(self.pack_info_list))
                if self.pack_info_list[i].get_show_str() == "N/A"
            ]
        self.assigned_pack_info_list = \
            [
                [
                    self.pack_info_list[j]
                    for j in range(len(self.pack_info_list))
                    if self.pack_info_list[j].get_show_str() != "N/A" and
                    self.pack_info_list[j].get_show_str() == ("%d" % (i + 1))
                ]
                for i in range(self.show_cnt)
            ]

        self._init_prompt()
        self.assigned_treeview.reconfigure_pack_cnt(
            len(self.assigned_pack_info_list[
                self.show_spinbox.get_show_num() - 1]))
        self.unassigned_treeview.reconfigure_pack_cnt(
            len(self.unassigned_pack_info_list))
        self._format_prompt()
        self._update_assigned_treeview()
        self._update_unassigned_treeview()

        if(destroy_command is not None):
            self.protocol("WM_DELETE_WINDOW", destroy_command)

    def _assign_pack_id(self):
        pack_idx = self._get_unassigned_pack_idx()
        if(pack_idx >= 0):
            show_num = self.show_spinbox.get_show_num()
            assigned_pack_info = self.unassigned_pack_info_list.pop(pack_idx)
            assigned_pack_info.set_pack_assignment(show_num - 1)
            self.assigned_pack_info_list[show_num - 1].append(
                assigned_pack_info)
            self._update_assigned_treeview()
            self._update_unassigned_treeview()
            self.assigned_treeview.focus(self.assigned_treeview.pack_iids[-1])
            self.assigned_treeview.selection_set(
                self.assigned_treeview.pack_iids[-1])

    def _format_prompt(self):
        width = self.winfo_width()
        height = self.winfo_height()
        screenwidth = self.sdt.master.winfo_screenwidth()
        screenheight = self.sdt.master.winfo_screenheight()

        self.minsize(width=width, height=width // 2)

        new_height = int(screenheight * 0.3)
        new_width = 2 * new_height
        if(new_height < width // 2):
            new_height = width // 2
        if(new_width < width):
            new_width = width

        new_x_pos = (screenwidth - new_width) // 2
        new_y_pos = (screenheight - new_height) // 2

        geometry_str = "{}x{}+{}+{}".format(new_width, new_height,
                                            new_x_pos, new_y_pos)

        self.geometry(geometry_str)
        self.update()

    def _get_assigned_pack_idx(self):
        curr_pack_iid = self.assigned_treeview.focus()
        curr_pack_idx = -1
        if(curr_pack_iid != ""):
            curr_pack_idx = self.assigned_treeview.index(curr_pack_iid)
        return curr_pack_idx

    def _get_unassigned_pack_idx(self):
        curr_pack_iid = self.unassigned_treeview.focus()
        curr_pack_idx = -1
        if(curr_pack_iid != ""):
            curr_pack_idx = self.unassigned_treeview.index(curr_pack_iid)
        return curr_pack_idx

    def _init_prompt(self):
        self.grid_rowconfigure(index=0, weight=5)
        self.grid_rowconfigure(index=1, weight=1)
        self.grid_rowconfigure(index=2, weight=1)
        self.grid_rowconfigure(index=3, weight=5)

        self.grid_columnconfigure(index=0, weight=1)
        self.grid_columnconfigure(index=1, weight=0)
        self.grid_columnconfigure(index=2, weight=0)
        self.grid_columnconfigure(index=3, weight=0)
        self.grid_columnconfigure(index=4, weight=1)
        self.grid_columnconfigure(index=5, weight=0)

        # Assigned Pack Setup
        # Pack Treeview for Assigned Packs
        self.assigned_treeview = SDTAssignTreeview(master=self, sdt=self.sdt)
        self.assigned_treeview.grid(in_=self,
                                    column=0,
                                    columnspan=1,
                                    row=0,
                                    rowspan=4,
                                    sticky="nswe")

        # Assigned Packs Scrollbar
        self.assigned_scrollbar = Scrollbar(
            master=self, command=self.assigned_treeview.yview)
        self.assigned_treeview.configure(
            yscrollcommand=self.assigned_scrollbar.set)
        self.assigned_scrollbar.grid(in_=self,
                                     column=1,
                                     row=0,
                                     rowspan=4,
                                     sticky="ns")

        # Middle Controls Setup
        # Alias Checkbox Setup
        self.alias_checkbox = Checkbutton(master=self,
                                          command=self._update_treeviews,
                                          text="Use Aliases?",
                                          variable=self.use_aliases)
        self.alias_checkbox.grid(in_=self,
                                 row=0,
                                 column=2,
                                 columnspan=2,
                                 sticky="s")

        # Show Label Setup
        self.show_label = Label(master=self, text="Show #")
        self.show_label.grid(in_=self,
                             row=1,
                             column=2,
                             sticky="e")

        # Show Spinbox Setup
        self.show_spinbox = SDTShowSpinbox(
            master=self,
            sdt=self.sdt,
            show_cnt=self.show_cnt,
            command=self._update_assigned_treeview)
        self.show_spinbox.grid(in_=self,
                               row=1,
                               column=3,
                               sticky="w")

        # Assign Pack ID Button Setup
        self.assign_button = Button(master=self,
                                    command=self._assign_pack_id,
                                    text="< Assign")
        self.assign_button.grid(in_=self,
                                column=2,
                                columnspan=2,
                                row=2,
                                sticky="")

        # Unassign Pack ID Button Setup
        self.unassign_setup = Button(master=self,
                                     command=self._unassign_pack_id,
                                     text="Unassign >")
        self.unassign_setup.grid(in_=self,
                                 column=2,
                                 columnspan=2,
                                 row=3,
                                 sticky="n")

        # Unassigned Pack Setup
        # Pack Treeview for Unassigned Packs
        self.unassigned_treeview = SDTAssignTreeview(master=self, sdt=self.sdt)
        self.unassigned_treeview.reconfigure_pack_cnt(
            len(self.unassigned_pack_info_list))
        self.unassigned_treeview.grid(in_=self,
                                      column=4,
                                      columnspan=1,
                                      row=0,
                                      rowspan=4,
                                      sticky="nswe")

        # Unassigned Packs Scrollbar
        self.unassigned_scrollbar = Scrollbar(
            master=self, command=self.unassigned_treeview.yview)
        self.unassigned_treeview.configure(
            yscrollcommand=self.unassigned_scrollbar.set)
        self.unassigned_scrollbar.grid(in_=self,
                                       column=5,
                                       row=0,
                                       rowspan=4,
                                       sticky="ns")

    def _on_destroy(self):
        self.destroy()

    def _unassign_pack_id(self):
        pack_idx = self._get_assigned_pack_idx()
        if(pack_idx >= 0):
            show_num = self.show_spinbox.get_show_num()
            unassigned_pack_info = \
                self.assigned_pack_info_list[show_num - 1].pop(pack_idx)
            unassigned_pack_info.set_pack_assignment(-1)
            self.unassigned_pack_info_list.append(unassigned_pack_info)
            self._update_assigned_treeview()
            self._update_unassigned_treeview()
            self.unassigned_treeview.focus(
                self.unassigned_treeview.pack_iids[-1])
            self.unassigned_treeview.selection_set(
                self.unassigned_treeview.pack_iids[-1])

    def _update_assigned_treeview(self):
        if(self.use_aliases.get()):
            assigned_pack_strs = \
                [
                    str(pack_info)
                    for pack_info
                    in self.assigned_pack_info_list[
                        self.show_spinbox.get_show_num() - 1]
                ]
        else:
            assigned_pack_strs = \
                [
                    pack_info.get_id_str()
                    for pack_info
                    in self.assigned_pack_info_list[
                        self.show_spinbox.get_show_num() - 1]
                ]
        self.assigned_treeview.reconfigure_pack_cnt(len(assigned_pack_strs))
        self.assigned_treeview.populate_pack_info_list(assigned_pack_strs)

    def _update_unassigned_treeview(self):
        if(self.use_aliases.get()):
            unassigned_pack_strs = \
                [
                    str(pack_info)
                    for pack_info in self.unassigned_pack_info_list
                ]
        else:
            unassigned_pack_strs = \
                [
                    pack_info.get_id_str()
                    for pack_info in self.unassigned_pack_info_list
                ]
        self.unassigned_treeview.reconfigure_pack_cnt(
            len(unassigned_pack_strs))
        self.unassigned_treeview.populate_pack_info_list(unassigned_pack_strs)

    def _update_treeviews(self):
        self._update_assigned_treeview()
        self._update_unassigned_treeview()
