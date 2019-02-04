from sdt_file_ops import SDTFileOps
from sdt_instr_ops import SDTInstrOps
from sdt_pack_ops import SDTPackOps
from sdt_set_ops import SDTSetOps
from sdt_show_ops import SDTShowOps
from tkinter.ttk import PanedWindow


class SDTOpRibbon(PanedWindow):
    # Static Variables
    ALIGN_LEFT = -1
    ALIGN_RIGHT = 1
    LAYOUT_NARROW = -1
    LAYOUT_STD = 0
    LAYOUT_WIDE = 1
    COLS = {
        LAYOUT_NARROW: 5,
        LAYOUT_STD: 7,
        LAYOUT_WIDE: 13
    }

    def __init__(self, master=None, sdt=None):
        PanedWindow.__init__(self, master, orient="horizontal")
        self.master = master
        self.sdt = sdt

        # Initialize Layout Variables
        self.layout_state = self.LAYOUT_NARROW
        self.column_width = 0
        self.curr_left_col = 0
        self.curr_right_col = self.COLS[self.layout_state]
        self.curr_row = 0
        self.widgets = []

        self._init_ribbon()

        # Bind method that updates layout based on the size allocated
        # to the SDTOpRibbon
        self.bind("<Configure>", self.configure_op_ribbon)

    def configure_op_ribbon(self, event):
        if(self.column_width == 0):
            self.column_width = self.winfo_width() // \
                self.COLS[self.layout_state] + 5

        if(event.widget is self and self.column_width > 0):
            new_width = event.width
            new_height = event.height

            if(new_width >= self.column_width * self.COLS[self.LAYOUT_WIDE]):
                self._update_layout(self.LAYOUT_WIDE)

            elif(self.column_width * self.COLS[self.LAYOUT_STD] <=
                 new_width < self.column_width * self.COLS[self.LAYOUT_WIDE]):
                self._update_layout(self.LAYOUT_STD)

            elif(new_width < self.column_width * self.COLS[self.LAYOUT_STD]):
                self._update_layout(self.LAYOUT_NARROW)

    def status_update(self, status_str):
        self.sdt.status_update(status_str)

    def _add(self, widget, alignment=ALIGN_LEFT):
        row = 0
        columnspan = 0
        column = 0

        if(alignment == self.ALIGN_RIGHT):
            columnspan = widget.get_columnspan()
            if(columnspan > self.COLS[self.layout_state]):
                columnspan = self.COLS[self.layout_state]

            if(columnspan > (self.curr_right_col - self.curr_left_col)):
                self.curr_row += 1
                self._reset_cols()

            row = self.curr_row
            column = self.curr_right_col - columnspan
            self.curr_right_col -= columnspan

            if(self.curr_left_col >= self.curr_right_col):
                self._reset_cols()
                self.curr_row += 1
        else:
            columnspan = widget.get_columnspan()
            if(columnspan > self.COLS[self.layout_state]):
                columnspan = self.COLS[self.layout_state]

            if(columnspan > (self.curr_right_col - self.curr_left_col)):
                self.curr_row += 1
                self._reset_cols()

            row = self.curr_row
            column = self.curr_left_col
            self.curr_left_col += columnspan

            if(self.curr_left_col >= self.curr_right_col):
                self._reset_cols()
                self.curr_row += 1

        self.widgets.append((widget, alignment))
        widget.grid(in_=self, row=row, column=column,
                    columnspan=columnspan, padx=5, pady=5, sticky="we")

    def _init_ribbon(self):
        # Global Show (File) Operations
        self.file_ops = SDTFileOps(master=self)
        self._add(self.file_ops, self.ALIGN_LEFT)

        # Individual Show Operations
        self.show_ops = SDTShowOps(master=self)
        self._add(self.show_ops, self.ALIGN_LEFT)

        # Set Operations
        self.set_ops = SDTSetOps(master=self)
        self._add(self.set_ops, self.ALIGN_LEFT)

        # Set Instruction Operations
        self.instr_ops = SDTInstrOps(master=self)
        self._add(self.instr_ops, self.ALIGN_LEFT)

        # Pack Operations
        self.pack_ops = SDTPackOps(master=self)
        self._add(self.pack_ops, self.ALIGN_RIGHT)

        for i in range(self.COLS[self.layout_state]):
            self.grid_columnconfigure(index=i, weight=1)

    def _reset_cols(self):
        self.curr_left_col = 0
        self.curr_right_col = self.COLS[self.layout_state]

    def _update_layout(self, new_state):
        for i in range(self.COLS[self.layout_state]):
            self.grid_columnconfigure(index=i, weight=0)

        self.layout_state = new_state

        self._reset_cols()
        self.curr_row = 0

        curr_widgets = self.widgets
        self.widgets = []
        for widget, alignment in curr_widgets:
            self._add(widget, alignment)

        for i in range(self.COLS[self.layout_state]):
            self.grid_columnconfigure(index=i, weight=1)
