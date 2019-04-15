from PIL import Image, ImageTk
from tkinter.ttk import Treeview


class SDTShowTreeview(Treeview):
    def __init__(self, master=None, sdt=None, set_cnt=1):
        Treeview.__init__(self, master, columns=("Red", "Green", "Blue"))
        self.sdt = sdt

        # Initialize Variables
        self.set_cnt = set_cnt
        self.set_iids = []  # Stores set iids within self
        # Stores PIL Images representing color previews
        self.color_imgs = []
        # Stores Tk PhotoImages representing color previews
        self.photo_imgs = []

        self._init_treeview()

        # Bind method that prevents users from resizing the set
        # instruction columns
        self.bind("<Button-1>", self._block_column_resize)

    def populate_set_instructions(self, individual_show=None):
        if(individual_show is not None):
            for i in range(self.set_cnt):
                self.item(self.set_iids[i],
                          values=individual_show.set_instructions[i])
                self.color_imgs[i].paste(individual_show.set_instructions[i],
                                         box=(0, 0) + self.color_imgs[i].size)
                self.photo_imgs[i] = ImageTk.PhotoImage(self.color_imgs[i])
                self.item(self.set_iids[i], image=self.photo_imgs[i])

    def reconfigure_set_cnt(self, new_set_cnt):
        self._adjust_set_cnt(new_set_cnt)

    def _add_set(self):
        size = 20
        color_img = Image.new("RGB", (size, size), color="black")
        self.color_imgs.append(color_img)
        photo_img = ImageTk.PhotoImage(color_img)
        self.photo_imgs.append(photo_img)
        new_set_iid = self.insert(parent="",
                                  index="end",
                                  image=photo_img,
                                  text="{}".format(len(self.set_iids) + 1),
                                  open=False)
        self.set_iids.append(new_set_iid)

    def _adjust_set_cnt(self, new_set_cnt):
        diff = new_set_cnt - self.set_cnt
        self.set_cnt = new_set_cnt
        if(diff > 0):
            for i in range(diff):
                self._add_set()
        elif(diff < 0):
            for i in range(-diff):
                tmp_set_iid = self.set_iids.pop()
                self.delete(tmp_set_iid)

    def _block_column_resize(self, event):
        if(self.identify_region(event.x, event.y) == "separator"):
            return "break"

    def _init_sets(self):
        for i in range(self.set_cnt):
            self._add_set()

    def _init_treeview(self):
        self.column("#0", anchor="center", minwidth=70,
                    stretch=False, width=70)
        self.column("Red", anchor="center", minwidth=70,
                    stretch=True, width=70)
        self.column("Green", anchor="center", minwidth=70,
                    stretch=True, width=70)
        self.column("Blue", anchor="center", minwidth=70,
                    stretch=True, width=70)

        self.heading("#0", anchor="center", text="Set #")
        self.heading("Red", anchor="center", text="Red")
        self.heading("Green", anchor="center", text="Green")
        self.heading("Blue", anchor="center", text="Blue")

        self._init_sets()
