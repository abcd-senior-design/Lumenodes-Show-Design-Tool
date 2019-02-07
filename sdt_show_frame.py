from sdt_individual_show import SDTIndividualShow
from sdt_show_spinbox import SDTShowSpinbox
from sdt_show_treeview import SDTShowTreeview
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

    def _add_new_show(self):
        show = SDTIndividualShow(
            master=self, sdt=self.sdt, set_cnt=self.set_cnt)
        self.individual_shows.append(show)

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
