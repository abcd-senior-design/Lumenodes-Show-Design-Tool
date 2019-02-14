from sdt_bounds import *
from sdt_individual_show import SDTIndividualShow
from sdt_show_spinbox import SDTShowSpinbox
from sdt_show_treeview import SDTShowTreeview
from tkinter import messagebox
from tkinter.ttk import Frame, Label, Scrollbar


class SDTShowFrame(Frame):
    def __init__(self, master=None, sdt=None, show_cnt=1, set_cnt=1):
        Frame.__init__(self, master)
        self.sdt = sdt

        # Initialize Variables
        self.show_cnt = show_cnt
        self.set_cnt = set_cnt
        self.individual_shows = []  # Stores SDTIndividualShow objects

        self._init_frame()

    def add_individual_show(self):
        success = False
        if(self.show_cnt < MAX_INDIVIDUAL_SHOW_CNT):
            success = True
            self._adjust_show_cnt(self.show_cnt + 1)
            self.show_spinbox.reconfigure_show_cnt(self.show_cnt)
        else:
            messagebox.showerror(
                "Error",
                "Maximum number of {} individual shows reached!".format(
                    MAX_INDIVIDUAL_SHOW_CNT),
                parent=self.sdt)
        return success, self.show_cnt

    def add_set(self):
        success = False
        if(self.set_cnt < MAX_SET_CNT):
            success = True
            self.set_cnt += 1
            for i in range(len(self.individual_shows)):
                self.individual_shows[i].add_set()
            self.show_treeview.reconfigure_set_cnt(self.set_cnt)
            self._update_show_treeview()
        else:
            messagebox.showerror(
                "Error",
                "Maximum number of {} sets reached!".format(
                    MAX_SET_CNT),
                parent=self.sdt)
        return success, self.set_cnt

    def clear_set_instruction(self):
        show_idx = self.show_spinbox.get_show_num() - 1
        set_idx = self._get_current_set_idx()
        success = False
        if(set_idx != -1):
            success = \
                self.individual_shows[show_idx].clear_set_instruction(set_idx)
            self._update_show_treeview()
        else:
            messagebox.showerror(
                "Error",
                "Please select set instruction to clear!",
                parent=self.sdt)
        return show_idx + 1, set_idx + 1

    def edit_set_instruction(self):
        show_idx = self.show_spinbox.get_show_num() - 1
        set_idx = self._get_current_set_idx()
        success = False
        if(set_idx != -1):
            success = \
                self.individual_shows[show_idx].edit_set_instruction(set_idx)
            self._update_show_treeview()
        else:
            messagebox.showerror(
                "Error",
                "Please select set instruction to edit!",
                parent=self.sdt)
        return success, show_idx + 1, set_idx + 1

    def get_show_info_list(self):
        show_info_list = []

        for i in range(self.show_cnt):
            show_info = self.individual_shows[i].get_show_info()
            show_info_list.append(show_info)

        return show_info_list

    def reconfigure_show_list(self, new_show_info_list,
                              new_show_cnt, new_set_cnt):
        self.set_cnt = new_set_cnt
        self._adjust_show_cnt(new_show_cnt)

        for i in range(self.show_cnt):
            self.individual_shows[i].reconfigure_show(
                new_show_info_list[i], new_set_cnt)

        self.show_treeview.reconfigure_set_cnt(self.set_cnt)
        self.show_spinbox.reconfigure_show_cnt(self.show_cnt)

        self._update_show_treeview()

    def remove_individual_show(self):
        show_num = self.show_spinbox.get_show_num()

        success = False
        if(self.show_cnt > MIN_INDIVIDUAL_SHOW_CNT):
            success = True
            self.individual_shows.pop(show_num - 1)
            self.show_cnt -= 1
            self.show_spinbox.reconfigure_show_cnt(self.show_cnt)
            self._update_show_treeview()
        elif(self.show_cnt == MIN_INDIVIDUAL_SHOW_CNT):
            success = messagebox.askokcancel(
                "Warning",
                "Removing last individual show.\n"
                "All set instructions will be cleared!",
                icon="warning",
                parent=self.sdt)
            if(success):
                self.show_cnt = 0
                self.individual_shows = []
                self._adjust_show_cnt(1)
                self.show_spinbox.reconfigure_show_cnt(self.show_cnt)
                self._update_show_treeview()
        return success, self.show_cnt, show_num

    def remove_set(self):
        success = False
        removed_set = -1
        if(self.set_cnt > MIN_SET_CNT):
            success = True
            self.set_cnt -= 1
            curr_set_idx = self._get_current_set_idx()

            for i in range(len(self.individual_shows)):
                self.individual_shows[i].remove_set(curr_set_idx)
            self.show_treeview.reconfigure_set_cnt(self.set_cnt)
            self._update_show_treeview()

            removed_set = curr_set_idx + 1
            if(removed_set <= 0):
                removed_set = self.set_cnt + 1
        else:
            messagebox.showerror(
                "Error",
                "Minimum number of {} sets reached!\n".format(
                    MIN_SET_CNT) +
                "Cannot remove any more sets!",
                parent=self.sdt)
        return success, self.set_cnt, removed_set

    def _add_new_show(self):
        show = SDTIndividualShow(
            master=self, sdt=self.sdt, set_cnt=self.set_cnt)
        self.individual_shows.append(show)

    def _adjust_show_cnt(self, new_show_cnt):
        diff = new_show_cnt - self.show_cnt
        self.show_cnt = new_show_cnt
        if(diff > 0):
            for i in range(diff):
                self._add_new_show()
        elif(diff < 0):
            for i in range(-diff):
                self.individual_shows.pop()

    def _get_current_set_idx(self):
        curr_set_iid = self.show_treeview.focus()
        curr_set_idx = -1
        if(curr_set_iid != ""):
            curr_set_idx = self.show_treeview.index(curr_set_iid)
        return curr_set_idx

    def _init_frame(self):
        self.grid_columnconfigure(index=0, weight=1)
        self.grid_columnconfigure(index=1, weight=1)
        self.grid_rowconfigure(index=1, weight=1)

        # Show Spinbox Label
        self.show_label = Label(master=self, text="Show #")
        self.show_label.grid(in_=self, row=0, column=0, sticky="e")

        # Show Spinbox
        self.show_spinbox = SDTShowSpinbox(master=self, sdt=self.sdt,
                                           show_cnt=self.show_cnt,
                                           command=self._update_show_treeview)
        self.show_spinbox.grid(in_=self, row=0, column=1, sticky="w")

        # Show Treeview
        self.show_treeview = SDTShowTreeview(
            master=self, sdt=self.sdt, set_cnt=self.set_cnt)
        self.show_treeview.grid(in_=self, row=1, column=0,
                                columnspan=2, sticky="nswe")

        # Show Scrollbar
        self.show_scrollbar = Scrollbar(
            master=self, command=self.show_treeview.yview)
        self.show_treeview.configure(yscrollcommand=self.show_scrollbar.set)
        self.show_scrollbar.grid(in_=self, row=1, column=2, sticky="ns")

        # Individual Show Wrappers
        self._init_shows()
        # Updates Show Treeview with currently selected show
        self._update_show_treeview()

    def _init_shows(self):
        for i in range(self.show_cnt):
            self._add_new_show()

    def _update_show_treeview(self):
        show_idx = self.show_spinbox.get_show_num() - 1
        self.show_treeview.populate_set_instructions(
            individual_show=self.individual_shows[show_idx])
        # Function must be called after the text variable is changed because
        # .set() disconnects the validate function
        self.show_spinbox._setup_validate()
