from tkinter import StringVar
from tkinter.ttk import Entry


class SDTPackIDEntry(Entry):
    def __init__(self, master=None, sdt=None):
        self.sdt = sdt
        self.pack_id = StringVar()
        self.pack_id.set("FF:FF:FF")

        Entry.__init__(self,
                       master,
                       textvariable=self.pack_id,
                       validate="all",
                       width=len(self.pack_id.get()))
        self.validatecommand = self.register(self.validate)
        self.config(validatecommand=(self.validatecommand, "%d", "%i", "%S"))

    def get_pack_id(self):
        pack_id = self.pack_id.get()
        try:
            return int(pack_id.replace(":", ""), 16)
        except:
            return -1

    def get_pack_id_str(self):
        return self.pack_id.get()

    def validate(self, why, where, what):
        needs_handled = True

        if(why == "0"):  # Attempted deletion
            string = self.pack_id.get()
            where_idx = int(where)
            what_len = len(what)

            if(not self.select_present()):
                # If the user has NOT selected an area of text, allow the
                # cursor to make negative progress (move the cursor backwards
                # with each keystroke) and backspace the hex digits of the
                # pack ID to "0"
                while(not string[where_idx].isalnum() and where_idx > 0):
                    where_idx -= 1
                if(string[where_idx].isalnum()):
                    string = string[:where_idx] + \
                        "0" + string[where_idx + 1:]
            else:
                # If the user HAS selected an area of text, place the cursor
                # at the beginning of that selection and "0" out all the
                # selected hex digits
                for i in range(what_len):
                    if(what[i].isalnum()):
                        string = string[:where_idx + i] + \
                            "0" + string[where_idx + i + 1:]
            self.pack_id.set(string)
            self.icursor(where_idx)
            self.selection_clear()
            needs_handled = False
        elif(why == "1"):   # Attempted insertion
            string = self.pack_id.get()
            where_idx = int(where)

            # Skip over non hex digits
            while(where_idx < len(string) and not string[where_idx].isalnum()):
                where_idx += 1

            # Update the desired portion of the string if the character
            # typed is a valid hex digit
            if(where_idx < len(string)):
                for i in range(len(what)):
                    if(self._ishexdigit(what[i])):
                        string = string[:where_idx + i] + \
                            what[i].upper() + string[where_idx + i + 1:]
                self.pack_id.set(string)
                self.icursor(where_idx + 1)

            self.selection_clear()
            needs_handled = False

        return needs_handled

    def _ishexdigit(self, character):
        if(character.isdigit()):
            return True
        elif(character == "A" or character == "a"):
            return True
        elif(character == "B" or character == "b"):
            return True
        elif(character == "C" or character == "c"):
            return True
        elif(character == "D" or character == "d"):
            return True
        elif(character == "E" or character == "e"):
            return True
        elif(character == "F" or character == "f"):
            return True
        return False
