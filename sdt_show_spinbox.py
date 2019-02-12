from math import log10
from tkinter import IntVar, Spinbox


class SDTShowSpinbox(Spinbox):
    def __init__(self, master=None, sdt=None, show_cnt=1, command=None):
        self.sdt = sdt

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

        # Bind FocusOut event to update the show number when the user leaves
        # the spinbox (which intuitively means that the user has edited the
        # number to satisfy their desire)
        self.bind("<FocusOut>", self._enter_spinbox)

        # Bind MouseWheel event to scroll the spinbox when the user scrolls
        # their mousewheel
        self.bind("<MouseWheel>", self._scroll_spinbox)

        # Bind Return event to update the show number when the user presses
        # the enter key (which intuitively means that the user has edited the
        # number to satisfy their desire)
        self.bind("<Return>", self._enter_spinbox)

        # Sets up the spinbox to verify that only numbers are being entered
        # into the spinbox.  This function must be called every time that a
        # spinbox action takes place to ensure that it continues to stay
        # linked appropriately.
        self._setup_validate()

    def get_show_num(self):
        return self.curr_show.get()

    def reconfigure_show_cnt(self, new_show_cnt):
        width = 2 * int(log10(new_show_cnt))
        self.configure(to=new_show_cnt)
        self.configure(width=width)
        self.show_cnt = new_show_cnt
        self.set_show_num(self.curr_show.get())

    def set_show_num(self, show_num=1):
        if(self.show_cnt > 1):
            self.curr_show.set(show_num - 1)
            self.invoke(element="buttonup")
        elif(self.show_cnt == 1):
            # This is necessary because when show_cnt == 1, then the bounds of
            # the Spinbox don't work properly
            self.curr_show.set(1)
        # Function must be called after the text variable is changed because
        # .set() disconnects the validate function
        self._setup_validate()

    def _enter_spinbox(self, event):
        self.set_show_num(show_num=self.curr_show.get())

    def _scroll_spinbox(self, event):
        increment = event.delta // 120
        new_value = self.curr_show.get() + increment - 1
        self.set_show_num(show_num=new_value)

    def _setup_validate(self):
        validatecommand = self.register(self._validate_input)
        self.configure(validate="all", validatecommand=(validatecommand, "%S"))

    def _validate_input(self, input_value):
        return input_value.isdigit()
