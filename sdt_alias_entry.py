from re import fullmatch, IGNORECASE
from tkinter import IntVar, Spinbox, StringVar
from tkinter.ttk import Button, Frame


class SDTAliasEntry(Frame):
    valid_symbols = tuple(
        [chr(i) for i in range(128) if (chr(i).isprintable() and
                                        (not chr(i).isspace()) and
                                        (not chr(i).isdigit()))
         ]
    )

    def __init__(self, master=None, sdt=None, alias=None,
                 command=None, destroy_command=None):
        Frame.__init__(self, master)
        self.sdt = sdt

        # Initialize Variables
        self.alias_symbol = StringVar()
        self.alias_number = IntVar()

        # Store off necessary commands
        self.command = command
        self.destroy_command = destroy_command

        self._init_alias_entry()
        self.alias_symbol.set("A")
        self._load_alias(alias)

        # Bind Esacpe event to escape and not save the input
        self.bind("<Escape>", self._escape_entry)
        # Bind FocusOut event to escape and save the input, assuming that
        # because the user clicked away that they are done editing
        self.bind("<FocusOut>", self._enter_entry)
        # Bind Return event to update the show number when the user presses
        # the enter key (which intuitively means that the user has edited the
        # contents to satisfy their desire)
        self.bind("<Return>", self._enter_entry)

    def extract_alias(alias):
        alias_symbol = None
        alias_number = None
        regex_str = (r"[" +
                     r"".join(SDTAliasEntry.valid_symbols) +
                     r"]" +
                     r"\d{1,2}")
        if(type(alias) is str):
            if(fullmatch(regex_str, alias, IGNORECASE)):
                alias_symbol = alias[0]
                alias_number = int(alias[1:])
        return alias_symbol, alias_number

    def _create_number_spinbox(self):
        self.number_spinbox = Spinbox(self,
                                      from_=1, to=99, increment=1,
                                      justify="center",
                                      textvariable=self.alias_number,
                                      width=6)

        # Bind Esacpe event to escape and not save the input
        self.number_spinbox.bind("<Escape>", self.destroy_command)

        # Bind MouseWheel event to scroll the selected spinbox when the user
        # scrolls their mousewheel
        self.number_spinbox.bind("<MouseWheel>", self._scroll_number_spinbox)

        # Bind Return event to update the show number when the user presses
        # the enter key (which intuitively means that the user has edited the
        # contents to satisfy their desire)
        self.number_spinbox.bind("<Return>", self._enter_entry)

    def _create_symbol_spinbox(self):
        self.symbol_spinbox = Spinbox(self,
                                      increment=1,
                                      justify="center",
                                      textvariable=self.alias_symbol,
                                      values=SDTAliasEntry.valid_symbols,
                                      width=6)

        # Bind Esacpe event to escape and not save the input
        self.symbol_spinbox.bind("<Escape>", self.destroy_command)

        # Bind MouseWheel event to scroll the selected spinbox when the user
        # scrolls their mousewheel
        self.symbol_spinbox.bind("<MouseWheel>", self._scroll_symbol_spinbox)

        # Bind Return event to update the show number when the user presses
        # the enter key (which intuitively means that the user has edited the
        # contents to satisfy their desire)
        self.symbol_spinbox.bind("<Return>", self._enter_entry)

    def _enter_entry(self, event):
        self.command()

    def _escape_entry(self, event):
        self.destroy_command()

    def _init_alias_entry(self):
        # Create Necessary Elements
        self._create_symbol_spinbox()
        self._create_number_spinbox()
        self.ok_button = Button(master=self,
                                command=self.command,
                                text=u"\U00002713",  # Unicode Checkmark
                                width=3)  # Keep this button small

        self.symbol_spinbox.grid(in_=self, row=0, column=0, sticky="we")
        self.number_spinbox.grid(in_=self, row=0, column=1, sticky="we")
        self.ok_button.grid(in_=self, row=0, column=2, sticky="")

        # Keep the button small, but allow the spinboxes to stretch
        self.columnconfigure(index=0, weight=1)
        self.columnconfigure(index=1, weight=1)
        self.columnconfigure(index=2, weight=0)

    def _load_alias(self, alias):
        alias_symbol, alias_number = SDTAliasEntry.extract_alias(alias)
        if(alias_symbol and alias_number):
            self.alias_symbol.set(alias_symbol)
            self.alias_number.set(alias_number)

    def _scroll_number_spinbox(self, event):
        increment = event.delta // 120
        new_value = self.alias_number.get() + increment - 1
        self.alias_number.set(new_value)
        self.number_spinbox.invoke("buttonup")

    def _scroll_symbol_spinbox(self, event):
        increment = event.delta // 120
        try:
            idx = SDTAliasEntry.valid_symbols.index(self.alias_symbol.get())
        except:
            self.symbol_spinbox.invoke("buttonup")
            idx = SDTAliasEntry.valid_symbols.index(self.alias_symbol.get())

        new_idx = (idx + increment)
        if(new_idx < 0):
            new_idx = 0
        elif(new_idx >= len(SDTAliasEntry.valid_symbols)):
            new_idx = len(SDTAliasEntry.valid_symbols) - 1
        self.alias_symbol.set(SDTAliasEntry.valid_symbols[new_idx])


staticmethod(SDTAliasEntry.extract_alias)
