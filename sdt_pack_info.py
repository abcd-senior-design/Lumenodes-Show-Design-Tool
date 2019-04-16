from sdt_bounds import PACK_ID_BYTES


class SDTPackInfo:
    def __init__(self, master=None, sdt=None, pack_id=0):
        self.master = master
        self.sdt = sdt

        # Initialize Pack Information
        self.pack_id = pack_id
        self.pack_alias_symbol = ""
        self.pack_alias_number = -1
        self.show_idx = -1

    def __str__(self):
        if(self.pack_alias_number == -1):
            return self.get_id_str()
        else:
            return self.get_alias_str()

    def get_info_tuple(self):
        return (self.get_id_str(), self.get_alias_str(), self.get_show_str())

    def get_alias_str(self):
        if(self.pack_alias_number == -1):
            return "N/A"
        else:
            return "%c%d" % (self.pack_alias_symbol, self.pack_alias_number)

    def get_id_str(self):
        hex_len = PACK_ID_BYTES * 2
        format_str = "%0{}X".format(hex_len)
        hex_str = (format_str % self.pack_id)[-hex_len:]

        hex_str_bytes = []
        for i in range(PACK_ID_BYTES):
            hex_str_bytes.append(hex_str[i * 2: (i + 1) * 2])
        return ":".join(hex_str_bytes)

    def get_pack_info(self):
        pack_info = {}
        pack_info["type"] = "pack_info"
        pack_info["pack_id"] = self.get_id_str()
        pack_info["pack_alias"] = self.get_alias_str()
        pack_info["pack_assignment"] = self.show_idx + 1
        return pack_info

    def get_show_str(self):
        if(self.show_idx == -1):
            return "N/A"
        else:
            return "%d" % (self.show_idx + 1)

    def set_pack_alias(self, alias_symbol, alias_number):
        self.pack_alias_symbol = alias_symbol
        self.pack_alias_number = alias_number

    def set_pack_assignment(self, show_idx):
        self.show_idx = show_idx
