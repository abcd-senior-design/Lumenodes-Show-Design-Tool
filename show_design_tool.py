from datetime import datetime
from sdt_op_ribbon import SDTOpRibbon
from tkinter import Tk
from tkinter.ttk import Frame, Label

import os


class ShowDesignTool(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master

        self.row_cnt = 0

        self.status_cnt = 0
        self.status_log = ""

        # Initializes Window to Most Compact Configuration
        self._init_window()
        # Forces Window to Update
        self.master.update()
        # Formats the Window to the Given Screensize and
        # stores off original configuration as minimum size
        self._format_window()

        # Intercepts Window Close to dump status log (for debugging)
        self.master.protocol("WM_DELETE_WINDOW", self._destroy_window)

    def dump_status_log(self):
        if(self.status_log):
            directory = ".status_logs"
            if(not os.path.isdir(directory)):
                try:
                    os.mkdir(directory)
                except:
                    return

            curr_time = datetime.today()
            filename = "status_log_" + \
                curr_time.strftime("%Y_%m_%d_%H_%M_%S") + ".txt"
            with open(directory + os.sep + filename, "w") as status_output:
                status_output.write(self.status_log)

    def status_update(self, status_str):
        self.status_cnt += 1
        new_status = "Status #{}: ".format(self.status_cnt) + status_str
        self.status_log += new_status + "\n"
        self.status_out.config(text=new_status)

    def _destroy_window(self):
        self.dump_status_log()
        try:
            self.master.destroy()
        except:
            pass

    def _format_window(self):
        self.master.minsize(self.master.winfo_width(),
                            self.master.winfo_height())

        width_prop = 0.7
        height_prop = 0.5

        # Resize to Decent Proportion of Window
        new_width = int(width_prop * self.master.winfo_screenwidth())
        new_height = int(height_prop * self.master.winfo_screenheight())
        new_x_pos = int((1 - width_prop) *
                        self.master.winfo_screenwidth() // 2)
        new_y_pos = int((1 - height_prop) *
                        self.master.winfo_screenheight() // 2)

        geometry_str = "{}x{}+{}+{}".format(new_width, new_height,
                                            new_x_pos, new_y_pos)

        self.master.geometry(geometry_str)

    def _init_window(self):
        # Initial Window Setup
        self.master.title("Lumenodes Show Design Tool")
        self.master.resizable(True, True)

        self.master.grid_columnconfigure(index=0, weight=1)
        self.master.grid_rowconfigure(index=0, weight=1)

        # Operation Ribbon Setup
        self.op_ribbon = SDTOpRibbon(master=self.master, sdt=self)
        self.op_ribbon.grid(in_=self.master, row=self.row_cnt, sticky="nwe")
        self.row_cnt += 1

        # Status Output
        self.status_out = Label(self.master, text="Status: [EMPTY]")
        self.status_out.grid(in_=self.master, row=self.row_cnt, sticky="s")
        self.row_cnt += 1

    def _op_ribbon_update(self, rowspan):
        # TODO: Adjust rows given to the op_ribbon based on how many
        # rows it actually needs
        pass


if __name__ == "__main__":
    root = Tk()
    show_design_tool = ShowDesignTool(root)
    root.mainloop()
