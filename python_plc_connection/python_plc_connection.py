# Following lines specifying, the location of DLLs, are required for Python Versions 3.8 and greater
import os
import imp
import time

# path_dll = r"C:\TwinCAT\AdsApi\TcAdsDll\x64\TcAdsDll.dll"
# print(path_dll)
# os.add_dll_directory(r"C:\TwinCAT\AdsApi\TcAdsDll\x64\TcAdsDll.dll")
# imp.load_dynamic("pyads", path_dll)
import pyads

# import pyads
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import ttk


class PythonPLCConnection(tk.Tk):
    def __init__(self):
        super().__init__()

        # region config form

        self.title("Python PLC Connection Test Application")

        # set columns width
        self.col_width = 30

        # set window size
        self.geometry(f"{self.col_width*15}x120")

        # set window color
        self.configure(bg="white")

        # Create frame
        self.frame = tk.Frame(self, bg="white")
        self.frame.pack(side="left", fill="both", expand=True)

        # endregion

        # region initialize plc

        # self.plc = pyads.Connection("192.168.126.1.1.1", 851)

        # endregion

        # region left upper frame items

        # Plc connection ip port title
        self.plc_connection_ip_port_title = tk.Label(
            self.frame,
            text="PLC connection ip & port:",
            anchor="w",
            bg="white",
            width=self.col_width,
        )
        self.plc_connection_ip_port_title.grid(row=0, column=0, sticky="w")

        # Plc connection ip textbox
        self.plc_connection_ip_textbox = tk.Text(
            self.frame, bg="white", height=1, width=int(self.col_width * 0.9 * 0.8)
        )
        self.plc_connection_ip_textbox.grid(row=0, column=1, sticky="w")
        self.plc_connection_ip_textbox.insert(0.0, "192.168.126.1.1.1")

        # Plc connection port textbox
        self.plc_connection_port_textbox = tk.Text(
            self.frame, bg="white", height=1, width=int(self.col_width * 0.9 * 0.2)
        )
        self.plc_connection_port_textbox.grid(row=0, column=1, sticky="e")
        self.plc_connection_port_textbox.insert(0.0, "851")

        # Start/Stop scanning button
        self.start_button = tk.Button(
            self.frame,
            text="Start",
            command=self.start_button_func,
            bg="white",
            width=self.col_width,
        )
        self.start_button.grid(row=1, column=0)

        # Start/Stop Scanning status and label
        self.start_button_status = tk.StringVar()
        self.start_button_status.set("Not started")
        self.start_button_status_label = tk.Label(
            self.frame,
            textvariable=self.start_button_status,
            anchor="w",
            bg="white",
            width=self.col_width,
        )
        self.start_button_status_label.grid(row=1, column=1, sticky="w")

        # Plc variable name title
        self.plc_variable_name_title = tk.Label(
            self.frame,
            text="PLC variable name:",
            anchor="w",
            bg="white",
            width=self.col_width,
        )
        self.plc_variable_name_title.grid(row=2, column=0, sticky="w")

        # Plc variable name textbox
        self.plc_variable_name_textbox = tk.Text(
            self.frame, bg="white", height=1, width=int(self.col_width * 0.9)
        )
        self.plc_variable_name_textbox.grid(row=2, column=1, sticky="w")
        self.plc_variable_name_textbox.insert(0.0, "global.bool_value")

        # Send variable to plc button
        self.send_variable_to_plc_button = tk.Button(
            self.frame,
            text="Send variable to plc",
            command=self.send_variable_to_plc_func,
            bg="white",
            width=self.col_width,
        )
        self.send_variable_to_plc_button.grid(row=3, column=0)

        # Send variable to plc textbox
        self.send_variable_to_plc_textbox = tk.Text(
            self.frame, bg="white", height=1, width=int(self.col_width * 0.9)
        )
        self.send_variable_to_plc_textbox.grid(row=3, column=1, sticky="w")
        self.send_variable_to_plc_textbox.insert(0.0, "False")

        # Read variable from plc button
        self.read_variable_from_plc_button = tk.Button(
            self.frame,
            text="Read variable from plc",
            command=self.read_variable_from_plc_func,
            bg="white",
            width=self.col_width,
        )
        self.read_variable_from_plc_button.grid(row=4, column=0)

        # Read variable from plc status and label
        self.read_variable_from_plc_status = tk.StringVar()
        self.read_variable_from_plc_status.set("Not read")
        self.read_variable_from_plc_status_label = tk.Label(
            self.frame,
            textvariable=self.read_variable_from_plc_status,
            anchor="w",
            bg="white",
            width=self.col_width,
        )
        self.read_variable_from_plc_status_label.grid(row=4, column=1, sticky="w")

        # endregion

    def start_button_func(self):
        if self.start_button["text"] == "Start":
            # Open plc connection
            self.plc = pyads.Connection(
                ams_net_id=self.plc_connection_ip_textbox.get(
                    index1="1.0", index2="end-1c"
                ).strip(),
                ams_net_port=int(
                    self.plc_connection_port_textbox.get(
                        index1="1.0", index2="end-1c"
                    ).strip()
                ),
            )
            self.plc.open()
            if self.plc.read_state():
                print(self.plc.read_state())
                self.start_button["text"] = "Stop"
                self.start_button_status.set("Started")
                self.start_button_status_label["bg"] = "darkolivegreen1"
        else:
            # Close plc connection
            self.plc.close()
            if self.plc.read_state() is None:
                print(self.plc.read_state())
                self.start_button["text"] = "Start"
                self.start_button_status.set("Stopped")
                self.start_button_status_label["bg"] = "indianred1"

    def send_variable_to_plc_func(self):
        self.plc.write_by_name(
            self.plc_variable_name_textbox.get(index1="1.0", index2="end-1c").strip(),
            self.InterpretVariable(
                self.send_variable_to_plc_textbox.get(
                    index1="1.0", index2="end-1c"
                ).strip()
            ),
        )
        self.read_variable_from_plc_func()

    def read_variable_from_plc_func(self):O
        self.read_variable_from_plc_status.set(
            str(
                self.plc.read_by_name(
                    self.plc_variable_name_textbox.get(
                        index1="1.0", index2="end-1c"
                    ).strip()
                )
            )
        )

    def InterpretVariable(self, var):
        if var in ["1", "True", "true", "TRUE"]:
            return True
        elif var in ["0", "False", "false", "TRUE"]:
            return False
        else:
            return var


if __name__ == "__main__":
    app = PythonPLCConnection()
    app.mainloop()
