from datetime import datetime
from sdt_op_ribbon import SDTOpRibbon
from sdt_show_frame import SDTShowFrame
from tkinter import Tk
from tkinter.ttk import Frame, Label

import os


class ShowDesignTool(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master

        # Initialize Layout Variables
        self.row_cnt = 0
        self.status_cnt = 0
        self.status_log = ""

        # Initialize Global Show Variables
        self.individual_show_cnt = 4
        self.set_cnt = 2

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
        minwidth = self.master.winfo_width()
        minheight = self.master.winfo_height()
        screenwidth = self.master.winfo_screenwidth()
        screenheight = self.master.winfo_screenheight()

        width_prop = 0.7
        height_prop = 0.5

        if(minwidth > screenwidth):
            minwidth = int(width_prop * screenwidth)
        if(minheight > screenheight):
            minheight = int(height_prop * screenheight)
        self.master.minsize(minwidth, minheight)

        # Resize to Decent Proportion of Window
        new_width = int(width_prop * screenwidth)
        new_height = int(height_prop * screenheight)
        new_x_pos = int((1 - width_prop) * screenwidth // 2)
        new_y_pos = int((1 - height_prop) * screenheight // 2)

        geometry_str = "{}x{}+{}+{}".format(new_width, new_height,
                                            new_x_pos, new_y_pos)

        self.master.geometry(geometry_str)

        # Prohibit each row (except the row that contains the individual
        # shows) from expanding after minimum size is determined
        # and the window is resized appropriately
        frame_row = self.show_frame.grid_info()['row']
        for i in range(self.row_cnt):
            if(i != frame_row):
                self.master.grid_rowconfigure(index=i, weight=0)

    def _init_window(self):
        # Initial Window Setup
        self.master.title("Lumenodes Show Design Tool")
        self.master.resizable(True, True)

        self.master.grid_columnconfigure(index=0, weight=1)

        # Operation Ribbon Setup
        self.op_ribbon = SDTOpRibbon(master=self.master, sdt=self)
        self.op_ribbon.grid(in_=self.master, row=self.row_cnt, sticky="n")
        self.row_cnt += 1

        # Individual Show Frame Setup
        self.show_frame = SDTShowFrame(master=self.master, sdt=self,
                                       show_cnt=self.individual_show_cnt,
                                       set_cnt=self.set_cnt)
        self.show_frame.grid(
            in_=self.master, row=self.row_cnt, sticky="nswe")
        self.row_cnt += 1

        # Status Output
        self.status_out = Label(self.master, text="Status: [EMPTY]")
        self.status_out.grid(in_=self.master, row=self.row_cnt, sticky="s")
        self.row_cnt += 1

        # Allow Each Row to expand appropriately to fit contents upon initial
        # creation of each element
        for i in range(self.row_cnt):
            self.master.grid_rowconfigure(index=i, weight=1)


if __name__ == "__main__":
    root = Tk()
    show_design_tool = ShowDesignTool(root)
    root.mainloop()
