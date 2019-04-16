from datetime import datetime
from sdt_op_ribbon import SDTOpRibbon
from sdt_pack_frame import SDTPackFrame
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

    def add_individual_show(self):
        success, new_show_cnt = self.show_frame.add_individual_show()
        self.individual_show_cnt = new_show_cnt
        return success

    def add_pack_id(self):
        self.pack_frame.add_pack_id()

    def add_set(self):
        success, new_set_cnt = self.show_frame.add_set()
        self.set_cnt = new_set_cnt
        return success

    def alias_pack_id(self):
        self.pack_frame.alias_pack_id()

    def assign_pack_id(self):
        return self.pack_frame.assign_pack_id()

    def clear_set_instruction(self):
        return self.show_frame.clear_set_instruction()

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

    def edit_set_instruction(self):
        return self.show_frame.edit_set_instruction()

    def get_global_show_info(self):
        global_show_info = {}
        global_show_info["type"] = "global_show"
        global_show_info["set_cnt"] = self.set_cnt
        global_show_info["individual_show_cnt"] = self.individual_show_cnt
        global_show_info["individual_shows"] = \
            self.show_frame.get_show_info_list()
        global_show_info["pack_info_list"] = \
            self.pack_frame.get_pack_info_list()
        return global_show_info

    def reconfigure_global_show(self, global_show_info):
        self.set_cnt = global_show_info["set_cnt"]
        self.individual_show_cnt = global_show_info["individual_show_cnt"]
        new_show_info_list = global_show_info["individual_shows"]
        self.show_frame.reconfigure_show_list(new_show_info_list,
                                              self.individual_show_cnt,
                                              self.set_cnt)
        new_pack_info_list = global_show_info["pack_info_list"]
        self.pack_frame.reconfigure_pack_list(new_pack_info_list)

    def remove_individual_show(self):
        success, new_show_cnt, removed_show = \
            self.show_frame.remove_individual_show()
        self.individual_show_cnt = new_show_cnt
        return success, removed_show

    def remove_pack_id(self):
        return self.pack_frame.remove_pack_id()

    def remove_set(self):
        success, new_set_cnt, removed_set = self.show_frame.remove_set()
        self.set_cnt = new_set_cnt
        return success, removed_set

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

        # Row 0 Setup
        # Operation Ribbon Setup
        self.op_ribbon = SDTOpRibbon(master=self.master, sdt=self)
        self.op_ribbon.grid(in_=self.master,
                            row=self.row_cnt,
                            column=0, columnspan=2,
                            sticky="n")

        # Row 0 Finished
        self.row_cnt += 1

        # Row 1 Setup
        # Individual Show Frame Setup
        self.show_frame = SDTShowFrame(master=self.master,
                                       sdt=self,
                                       set_cnt=self.set_cnt,
                                       show_cnt=self.individual_show_cnt)
        self.show_frame.grid(in_=self.master,
                             row=self.row_cnt,
                             column=0,
                             sticky="nswe")

        # Pack ID Frame Setup
        self.pack_frame = SDTPackFrame(master=self.master, sdt=self)
        self.pack_frame.grid(in_=self.master,
                             row=self.row_cnt,
                             column=1,
                             sticky="nswe")

        # Row 1 Finished
        self.row_cnt += 1

        # Row 2 Setup
        # Status Output
        self.status_out = Label(self.master, text="Status: [EMPTY]")
        self.status_out.grid(in_=self.master,
                             row=self.row_cnt,
                             column=0, columnspan=2,
                             sticky="s")

        # Row 2 Finished
        self.row_cnt += 1

        # Allow Each Row to expand appropriately to fit contents upon initial
        # creation of each element
        for i in range(self.row_cnt):
            self.master.grid_rowconfigure(index=i, weight=1)

        # Allow the Show Frame to grow twice as quickly than the Pack Frame
        # (width-wise), to emphasize that the Show Frame is the primary focus
        show_frame_row = self.show_frame.grid_info()['column']
        pack_frame_row = self.pack_frame.grid_info()['column']
        self.master.grid_columnconfigure(index=show_frame_row, weight=2)
        self.master.grid_columnconfigure(index=pack_frame_row, weight=1)


if __name__ == "__main__":
    root = Tk()
    show_design_tool = ShowDesignTool(root)
    root.mainloop()
