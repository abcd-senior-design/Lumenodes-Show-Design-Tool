from math import log10
from tkinter import IntVar, Spinbox


class SDTShowSpinbox(Spinbox):
    def __init__(self, master=None, show_cnt=1, command=None):
        # Initialize Variables
        self.curr_show = IntVar()
        self.curr_show.set(1)
        self.show_cnt = show_cnt
        width = 2 * int(log10(self.show_cnt))

        Spinbox.__init__(self, master,
                         from_=1, to=self.show_cnt, increment=1,
                         command=command,
                         textvariable=self.curr_show,
                         width=width)

    def get_show_num(self):
        return self.curr_show.get()

    def set_show_num(self, show_num=1):
        if(self.show_cnt > 1):
            self.curr_show.set(show_num - 1)
            self.invoke(element="buttonup")
        elif(self.show_cnt == 1):
            # This is necessary because when show_cnt == 1, then the bounds of
            # the Spinbox don't work properly
            self.curr_show.set(1)
