from sdt_bounds import PACK_ID_BYTES


class SDTPackInfo:
    def __init__(self, master=None, sdt=None, pack_id=0):
        self.master = master
        self.sdt = sdt

        # Initialize Pack Information
        self.pack_id = pack_id

    def __str__(self):
        return self.get_id_str()

    def get_info_tuple(self):
        return (self.get_id_str(),)

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
        return pack_info
