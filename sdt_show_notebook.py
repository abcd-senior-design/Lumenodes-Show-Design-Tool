from sdt_individual_show import SDTIndividualShow
from tkinter.ttk import Notebook


class SDTShowNotebook(Notebook):
    def __init__(self, master=None, show_cnt=1, set_cnt=1):
        Notebook.__init__(self, master)
        self.master = master

        # Initialize Variables
        self.show_cnt = show_cnt
        self.set_cnt = set_cnt
        self.curr_show = -1
        self.shows = []

        self._init_notebook()

        # Bind method that ensures each indvidiual show effectively
        # scrolls "in tandem" by updating the newly selected tab to scroll
        # to where the previously selected tab was located
        self.bind("<<NotebookTabChanged>>", self._udpate_show_scroll)

    def add_new_show(self):
        show = SDTIndividualShow(master=self, set_cnt=self.set_cnt)
        self.shows.append(show)
        self.add(show, text="Show {}".format(len(self.shows)), sticky="nswe")

    def _init_notebook(self):
        for i in range(self.show_cnt):
            self.add_new_show()

    def _udpate_show_scroll(self, event):
        if(self.curr_show == -1):
            self.curr_show = self.index(self.select())
        else:
            prev_show = self.curr_show
            a, b = self.shows[prev_show].scrollbar.get()
            self.curr_show = self.index(self.select())
            self.shows[self.curr_show].treeview.yview("moveto", a)
