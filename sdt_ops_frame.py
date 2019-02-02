from tkinter.ttk import LabelFrame


class SDTOpsFrame(LabelFrame):
    def __init__(self, master=None, text="Operations"):
        LabelFrame.__init__(
            self, master, text=text, labelanchor="se")
        self.master = master
        self.column_cnt = 0

    def get_columnspan(self):
        return self.column_cnt

    def _add(self, button):
        button.grid(in_=self, row=0, column=self.column_cnt, sticky="we")
        self.grid_columnconfigure(index=self.column_cnt, weight=1)
        self.column_cnt += 1
