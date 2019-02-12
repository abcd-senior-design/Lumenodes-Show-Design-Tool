from functools import partial
from sdt_ops_frame import SDTOpsFrame
from tkinter import filedialog
from tkinter.ttk import Button

import json
import os
import zipfile


class SDTFileOps(SDTOpsFrame):
    def __init__(self, master=None, sdt=None):
        SDTOpsFrame.__init__(self, master=master, sdt=sdt,
                             text="File Operations")

        self._init_ops()

    def create_new_file(self):
        self._sdt_status_update("Create New File")

    def open_file(self):
        # Prompt User for Desired Filename
        filename = self._get_filename("Open")

        if(filename != ""):
            global_show_json = ""
            if(filename.endswith(".zip")):
                global_show_json = self._read_zip_archive(filename)
            elif(filename.endswith(".json")):
                global_show_json = self._read_json_file(filename)

            global_show_info = None
            if(global_show_json != ""):
                try:
                    # Convert json object to a Global Show Info dictionary
                    global_show_info = json.loads(global_show_json)
                except:
                    self._sdt_status_update("")
                    global_show_info = None

            short_filename = os.path.basename(filename)
            base_error_string = "Error! Could not open {}! ".format(
                short_filename)
            success = False
            if(global_show_info is not None):
                success = self._reconfigure_sdt(
                    global_show_info, base_error_string)

            if(success):
                self._sdt_status_update(
                    "Successfully opened '{}'".format(short_filename))

    def save_file(self):
        # Prompt User for Desired Filename
        filename = self._get_filename("Save As")

        if(filename != ""):
            # Retreive Global Show Information (in a dictionary)
            global_show_info = self.sdt.get_global_show_info()

            # Convert Global Show Dictionary to a json object
            global_show_json = json.dumps(
                global_show_info, indent=4, sort_keys=True)

            success = False
            if(filename.endswith(".zip")):
                succcess = self._write_zip_archive(filename, global_show_json)
            elif(filename.endswith(".json")):
                succcess = self._write_json_file(filename, global_show_json)

            short_filename = os.path.basename(filename)
            if(success):
                self._sdt_status_update(
                    "Successfully saved '{}'".format(short_filename))

    def _get_filename(self, op_title):
        filename = ""

        json_file_type = ("JavaScript Object Notation File", ".json")
        zip_file_type = ("Compressed Zip Archive", ".zip")
        filetypes = [zip_file_type, json_file_type]

        if("Open" in op_title):
            filename = filedialog.askopenfilename(
                defaultextension=".zip",
                filetypes=filetypes,
                initialdir="." + os.sep + "global_shows",
                title="Open")
        elif("Save" in op_title):
            filename = filedialog.asksaveasfilename(
                defaultextension=".zip",
                filetypes=filetypes,
                initialdir="." + os.sep + "global_shows",
                initialfile="MyGlobalShow",
                title="Save As")

        return filename

    def _init_ops(self):
        # Global Show (File) Operations
        self.new_file_button = Button(
            self, text="New", command=partial(self.create_new_file))
        self._add(self.new_file_button)

        self.open_file_button = Button(
            self, text="Open", command=partial(self.open_file))
        self._add(self.open_file_button)

        self.save_file_button = Button(
            self, text="Save", command=partial(self.save_file))
        self._add(self.save_file_button)

    def _open_zip_archive(self, filename, mode="r"):
        zip_archive = zipfile.ZipFile(
            file=filename, mode=mode, compression=zipfile.ZIP_DEFLATED)
        return zip_archive

    def _read_json_file(self, filename):
        global_show_json = ""
        try:
            with open(filename, "r") as input_file:
                global_show_json = input_file.read()
        except:
            self._sdt_status_update(
                "Error reading \"{}\"!".format(os.path.basename(filename)))
        return global_show_json

    def _read_zip_archive(self, filename):
        global_show_json = ""
        try:
            with self._open_zip_archive(filename, "r") as input_archive:
                global_show_json = input_archive.read("global_show_info.json")
        except:
            self._sdt_status_update(
                "Error extracting and reading \"{}\"!".format(
                    os.path.basename(filename)))
        return global_show_json

    def _reconfigure_sdt(self, global_show_info, base_error_string):
        success = False

        if(self._verify_global_show(global_show_info, base_error_string)):
            # Set Global Show Information (from a dictionary)
            self.sdt.reconfigure_global_show(global_show_info)
            success = True

        return success

    def _verify_global_show(self, global_show_info, base_error_string):
        global_show_verified = False

        if(type(global_show_info) is not dict):
            self._sdt_status_update(base_error_string +
                                    "Global show info failed to convert to "
                                    "a dictionary!")
        elif("type" not in global_show_info):
            self._sdt_status_update(base_error_string +
                                    "Global show info is incorrectly "
                                    "formatted! 'type' is missing!")
        elif(global_show_info["type"] != "global_show"):
            self._sdt_status_update(base_error_string +
                                    "Global show info is incorrectly "
                                    "formatted! 'type' is '{}'!".format(
                                        global_show_info["type"]))
        elif("set_cnt" not in global_show_info):
            self._sdt_status_update(base_error_string +
                                    "Global show info is incorrectly "
                                    "formatted! 'set_cnt' is missing!")
        elif("individual_show_cnt" not in global_show_info):
            self._sdt_status_update(base_error_string +
                                    "Global show info is incorrectly "
                                    "formatted! 'individual_show_cnt' is "
                                    "missing!")
        elif("individual_shows" not in global_show_info):
            self._sdt_status_update(base_error_string +
                                    "Global show info is incorrectly "
                                    "formatted! "
                                    "'individual_shows' is missing!")
        else:
            new_set_cnt = global_show_info["set_cnt"]
            new_show_cnt = global_show_info["individual_show_cnt"]
            new_show_info_list = global_show_info["individual_shows"]

            if(new_set_cnt <= 0):
                self._sdt_status_update(base_error_string +
                                        "Global show contains invalid data! "
                                        "Set count is not positive!")
            elif(new_show_cnt <= 0):
                self._sdt_status_update(base_error_string +
                                        "Global show contains invalid data! "
                                        "Show count is not positive!")
            elif(new_show_cnt != len(new_show_info_list)):
                self._sdt_status_update(base_error_string +
                                        "Global show contains invalid data! "
                                        "Show count does not match the number "
                                        "of shows!")
            else:
                show_verified = True
                for i in range(new_show_cnt):
                    show_verified = self._verify_individual_show(
                        new_show_info_list[i], new_set_cnt, base_error_string)
                    if(not show_verified):
                        break
                global_show_verified = show_verified

        return global_show_verified

    def _verify_individual_show(self, individual_show_info,
                                new_set_cnt, base_error_string):
        show_verified = False
        correct_format = ("type" in individual_show_info and
                          "set_instructions" in individual_show_info)

        if("type" not in individual_show_info):
            self._sdt_status_update(base_error_string +
                                    "Individual show info is incorrectly "
                                    "formatted! 'type' is missing!")
        elif(individual_show_info["type"] != "individual_show"):
            self._sdt_status_update(base_error_string +
                                    "Individual show info is incorrectly "
                                    "formatted! 'type' is '{}'!".format(
                                        individual_show_info["type"]))
        elif("set_instructions" not in individual_show_info):
            self._sdt_status_update(base_error_string +
                                    "Individual show info is incorrectly "
                                    "formatted! 'set_instructions' is "
                                    "missing!")
        else:
            new_set_instructions = individual_show_info["set_instructions"]

            if(new_set_cnt != len(new_set_instructions)):
                self._sdt_status_update(base_error_string +
                                        "Individual show contains invalid "
                                        "data! Set count does not match the "
                                        "number of sets!")
            else:
                set_instruction_verified = True
                for i in range(new_set_cnt):
                    set_instruction_verified = self._verify_set_instruction(
                        new_set_instructions[i], base_error_string)
                    if(not set_instruction_verified):
                        break
                show_verified = set_instruction_verified

        return show_verified

    def _verify_set_instruction(self, set_instruction_info, base_error_string):
        set_instruction_verified = False
        if("type" not in set_instruction_info):
            self._sdt_status_update(base_error_string +
                                    "Set instruction info is incorrectly "
                                    "formatted! 'type' is missing!")
        elif(set_instruction_info["type"] != "set_instruction"):
            self._sdt_status_update(base_error_string +
                                    "Set instruction info is incorrectly "
                                    "formatted! 'type' is '{}'!".format(
                                        set_instruction_info["type"]))
        elif("r" not in set_instruction_info):
            self._sdt_status_update(base_error_string +
                                    "Set instruction info is incorrectly "
                                    "formatted! 'r' is missing!")
        elif("g" not in set_instruction_info):
            self._sdt_status_update(base_error_string +
                                    "Set instruction info is incorrectly "
                                    "formatted! 'g' is missing!")
        elif("b" not in set_instruction_info):
            self._sdt_status_update(base_error_string +
                                    "Set instruction info is incorrectly "
                                    "formatted! 'b' is missing!")
        else:
            set_instruction_verified = True

        return set_instruction_verified

    def _write_json_file(self, filename, global_show_json):
        success = False
        try:
            with open(filename, "w") as output_file:
                output_file.write(global_show_json)
            success = True
        except:
            self._sdt_status_update(
                "Error creating and writing \"{}\"!".format(
                    os.path.basename(filename)))
        return success

    def _write_zip_archive(self, filename, global_show_json):
        success = False
        try:
            with self._open_zip_archive(filename, "w") as output_archive:
                output_archive.writestr(
                    "global_show_info.json", global_show_json)
            success = True
        except:
            self._sdt_status_update(
                "Error creating and writing \"{}\"!".format(
                    os.path.basename(filename)))
        return success
