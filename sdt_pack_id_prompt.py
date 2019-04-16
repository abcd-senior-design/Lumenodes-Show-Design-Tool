from tkinter import Toplevel
from tkinter.ttk import Button, Label

from sdt_pack_id_entry import SDTPackIDEntry


class SDTPackIDPrompt(Toplevel):
    def __init__(self, master=None, sdt=None, command=None):
        Toplevel.__init__(self, master)
        self.title("Add Pack ID")
        self.resizable(False, False)
        self.transient(self.master)  # Keeps prompt under same taskbar icon
        self.focus()  # Forces focus to be on this prompt
        # Grabs all events from other window, preventing interaction with
        # main window while the prompt is open
        self.grab_set()
        self.lift()  # Brings this window to the top of the window stack

        self.sdt = sdt
        self.command = command

        self.bind("<Return>", self._enter_entry)
        self._init_prompt()
        self._format_prompt()
        self.pack_id_entry.focus()
        self.pack_id_entry.icursor("end")

    def get_pack_id(self):
        return self.pack_id_entry.get_pack_id()

    def get_pack_id_str(self):
        return self.pack_id_entry.get_pack_id_str()

    def _enter_entry(self, event):
        self.command()

    def _format_prompt(self):
        width = self.winfo_width()
        height = self.winfo_height()
        screenwidth = self.sdt.master.winfo_screenwidth()
        screenheight = self.sdt.master.winfo_screenheight()

        self.minsize(width=width, height=width // 2)

        new_height = int(screenheight * 0.15)
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
        self.pack_id_label.config(wraplength=self.winfo_width())

    def _init_prompt(self):
        self.grid_rowconfigure(index=0, weight=1)
        self.grid_rowconfigure(index=1, weight=1)
        self.grid_rowconfigure(index=2, weight=1)

        self.grid_columnconfigure(index=0, weight=1)
        self.grid_columnconfigure(index=1, weight=1)
        self.grid_columnconfigure(index=2, weight=1)
        self.grid_columnconfigure(index=3, weight=1)

        # Label Setup
        self.pack_id_label = Label(master=self,
                                   text="Please enter the new Pack ID below",
                                   anchor="center",
                                   justify="center")
        self.pack_id_label.grid(in_=self,
                                column=0,
                                columnspan=4,
                                row=0,
                                sticky="nswe")

        # Pack ID Entry Setup
        self.pack_id_entry = SDTPackIDEntry(master=self, sdt=self.sdt)
        self.pack_id_entry.grid(in_=self,
                                column=1,
                                columnspan=2,
                                row=1,
                                sticky="")
        self.pack_id_entry.bind("<Return>", self._enter_entry)

        # OK Button Setup
        self.ok_button = Button(master=self,
                                command=self.command,
                                text="OK")
        self.ok_button.grid(in_=self,
                            column=1,
                            row=2)

        # Cancel Button Setup
        self.cancel_button = Button(master=self,
                                    command=self.destroy,
                                    text="Cancel")
        self.cancel_button.grid(in_=self,
                                column=2,
                                row=2)
