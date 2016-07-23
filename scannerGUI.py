# -*- coding: utf-8 -*-

# build the scanner window
import settings
import scanner
import network
import ipaddress
from tkinter import *


# Scanner GUI
class scanner_gui(object):

    def __init__(self):
        pass

    def show(self):
        """show the scanner window"""
        if not settings.gui_scanner_window_open:
            settings.gui_scanner_window_open = True
            self.build_window()

    def close(self):
        """close the scanner window"""
        self.scan_stop()  # just in cause one is running
        self.window.destroy()
        settings.gui_scanner_window_open = False

    def build_window(self):
        """draw the scanner window"""
        # main window
        self.window = Toplevel()
        self.window.title("Lanmap - Network Scanner")
        self.window.geometry("702x505")
        self.window.protocol("WM_DELETE_WINDOW", self.close)

        # 2 frames and layout
        self.left_frame = Frame(self.window)
        self.left_frame.pack(side=LEFT, fill=Y)
        self.right_frame = Frame(self.window, bd=1)
        self.right_frame.pack(side=LEFT, fill=BOTH, padx=5, pady=5)
        self.left_top_frame = Frame(self.left_frame, bd=1, relief=SUNKEN,
            pady=5)
        self.left_top_frame.pack(side=TOP, fill=X)
        self.left_bottom_frame = Frame(self.left_frame, bd=1, relief=SUNKEN)
        self.left_bottom_frame.pack(side=TOP, fill=BOTH, expand=1)

        # 3 select scan mode buttons
        self.scan_mode = IntVar()
        self.scan_mode_ipv4_button = Radiobutton(self.left_top_frame,
            text="IPv4 Scan", variable=self.scan_mode,
            value=0, indicatoron=0, height=2, padx=13)
        self.scan_mode_ipv4_button.pack(side=LEFT, padx=2)
        self.scan_mode_ipv4_button.bind("<Button-1>", self.switch_to_ipv4)
        self.scan_mode_ipv6_button = Radiobutton(self.left_top_frame,
            text="IPv6 Scan", variable=self.scan_mode,
            value=1, indicatoron=0, height=2, padx=13)
        self.scan_mode_ipv6_button.pack(side=LEFT, padx=0)
        self.scan_mode_ipv6_button.bind("<Button-1>", self.switch_to_ipv6)

        # 4 IPv4 scan settings
        self.ipv4_preset_name = StringVar()
        self.ipv4_start_ip = StringVar()
        self.ipv4_stop_ip = StringVar()
        self.ipv4_get_hostnames = IntVar()
        self.ipv4_timeout = StringVar()
        self.ipv4_scanner = Frame(self.left_bottom_frame, borderwidth=2,
            height=500)
        self.ipv4_scanner.pack()
        self.ipv4_title = Label(self.ipv4_scanner, text="IPv4 Scan Settings",
                pady=12)
        self.ipv4_title.pack(side=TOP, fill=X)
        self.ipv4_presets_title = Label(self.ipv4_scanner, text="Presets:",
                pady=5, anchor=SW)
        self.ipv4_presets_title.pack(side=TOP, fill=X)
        self.ipv4_presets_list = Listbox(self.ipv4_scanner, height=4, width=21)
        self.ipv4_presets_list.pack(side=TOP, fill=X, expand=1)
        self.ipv4_presets_controls = Frame(self.ipv4_scanner)
        self.ipv4_presets_controls.pack(side=TOP, fill=X, ipadx=0,
            ipady=1, expand=1)
        self.ipv4_presets_delete_button = Button(self.ipv4_presets_controls,
                text="−", command=self.delete_preset)
        self.ipv4_presets_delete_button.pack(side=RIGHT)
        self.ipv4_presets_add_button = Button(self.ipv4_presets_controls,
                text="+", command=self.add_preset)
        self.ipv4_presets_add_button.pack(side=RIGHT)
        self.ipv4_preset_name = Label(self.ipv4_scanner,
            text="Preset name:", pady=4)
        self.ipv4_preset_name.pack(side=TOP, anchor=SW)
        self.ipv4_preset_name_entry = Entry(self.ipv4_scanner,
                textvariable=self.ipv4_preset_name, width=21)
        self.ipv4_preset_name_entry.pack(side=TOP)
        self.ipv4_start_ip_label = Label(self.ipv4_scanner,
            text="Start range IP:", pady=4)
        self.ipv4_start_ip_label.pack(side=TOP, anchor=SW,)
        self.ipv4_start_ip_entry = Entry(self.ipv4_scanner,
            textvariable=self.ipv4_start_ip, width=21)
        self.ipv4_start_ip_entry.pack(side=TOP)
        self.ipv4_stop_ip_label = Label(self.ipv4_scanner,
            text="Stop range IP:", pady=4)
        self.ipv4_stop_ip_label.pack(side=TOP, anchor=SW,)
        self.ipv4_stop_ip_entry = Entry(self.ipv4_scanner,
            textvariable=self.ipv4_stop_ip, width=21)
        self.ipv4_stop_ip_entry.pack(side=TOP)
        self.ipv4_get_hostnames_checkbutton = Checkbutton(self.ipv4_scanner,
                text=" Get hostnames", var=self.ipv4_get_hostnames,
                anchor=W)
        self.ipv4_get_hostnames_checkbutton.pack(side=TOP, fill=X,
            pady=4, padx=1)
        self.ipv4_timeout_label = Label(self.ipv4_scanner,
            text="Ping timeout in seconds:", anchor=W)
        self.ipv4_timeout_label.pack(side=TOP, pady=4, anchor=NW)
        self.ipv4_timeout_entry = Spinbox(self.ipv4_scanner,
            textvariable=self.ipv4_timeout, from_=1, to=5, width=4)
        self.ipv4_timeout_entry.pack(side=TOP, padx=0, anchor=W)
        self.ipv4_scan_button = Button(self.ipv4_scanner,
            text="Start Scan", height=4, command=self.scan_ipv4)
        self.ipv4_scan_button.pack(side=BOTTOM, fill=X, padx=3, pady=10)

        # IPv6 Scan Settings
        self.ipv6_scanner = Frame(self.left_bottom_frame, borderwidth=2)
        self.ipv6_title = Label(self.ipv6_scanner, text="IPv6 Scan Settings",
                pady=12)
        self.ipv6_title.pack(side=TOP, fill=X)
        self.ipv6_presets_title = Label(self.ipv6_scanner,
            text="Choose Interface:", pady=5, anchor=SW)
        self.ipv6_presets_title.pack(side=TOP, fill=X)
        self.ipv6_presets_list = Listbox(self.ipv6_scanner, height=10,
            width=21)
        self.ipv6_presets_list.pack(side=TOP, fill=X, expand=1)
        self.ipv6_get_hostnames_checkbutton = Checkbutton(self.ipv6_scanner,
                text=" Get hostnames", var=self.ipv4_get_hostnames,
                anchor=W)
        self.ipv6_get_hostnames_checkbutton.pack(side=TOP, fill=X,
            pady=4, padx=1)
        self.ipv6_timeout_label = Label(self.ipv6_scanner,
            text="Ping timeout in seconds:", anchor=W)
        self.ipv6_timeout_label.pack(side=TOP, pady=4, anchor=NW)
        self.ipv6_timeout_entry = Spinbox(self.ipv6_scanner,
            textvariable=self.ipv4_timeout, from_=1, to=5, width=4)
        self.ipv6_timeout_entry.pack(side=TOP, padx=0, anchor=W)
        self.ipv6_scan_button = Button(self.ipv6_scanner,
            text="Start Scan", height=4)
        self.ipv6_scan_button.pack(side=BOTTOM, fill=X, padx=3, pady=10)

        # Result command frame
        self.results_commands = Frame(self.right_frame, height=30,
            width=487)
        self.results_commands.pack(side=BOTTOM, fill=X)
        self.clear_results = 0
        self.clear_selected = 0
        self.add_results = 0
        self.add_selected = 0

        # Result list
        self.results = Canvas(self.right_frame, background="#EEEEEE",
            scrollregion=(0, 0, 490, 1800), width=510, relief=SUNKEN)
        self.results_scrollbar = Scrollbar(self.right_frame,
            orient="vertical", command=self.results.yview)
        self.results_scrollbar.pack(side=RIGHT, fill=Y)
        self.results.configure(yscrollcommand=self.results_scrollbar.set)
        self.results.pack(side=LEFT, fill=BOTH, expand=1)

        # header row of results list
        self.results.create_rectangle(1, 1, 489, 36, fill="#EEF4B2")
        self.results.create_line(1, 37, 490, 37, width=3)
        self.results.create_text(14, 13, text="[ ]", anchor=NW)
        self.results.create_text(39, 13, text="Ip addresses", anchor=NW)
        self.results.create_text(166, 13, text="Name", anchor=NW)
        self.results.create_text(301, 13, text="Parents ip('s)", anchor=NW)
        self.results.create_text(428, 13, text="Add node", anchor=NW)

# class functions

    def switch_to_ipv4(self, event):
        """if the ipv4 scan button is pressed, adjust tkinter widgets"""
        self.ipv4_scanner.pack()
        self.ipv6_scanner.pack_forget()

    def switch_to_ipv6(self, event):
        """if the ipv6 scan button is pressed, adjust tkinter widgets"""
        self.ipv4_scanner.pack_forget()
        self.ipv6_scanner.pack()

    def scan_ipv4(self):
        """start a ipv4 scan"""
        # some input validation
        start = self.ipv4_start_ip.get()
        stop = self.ipv4_stop_ip.get()
        if not network.is_valid_ip4(start):
            self.ipv4_start_ip_entry.config(background="red")
        else:
            self.ipv4_start_ip_entry.config(background="white")
        if start and stop:
            a = ipaddress.IPv4Address(start)
            b = ipaddress.IPv4Address(stop)
        if not network.is_valid_ip4(stop) or a > b:
            self.ipv4_stop_ip_entry.config(background="red")
        else:
            self.ipv4_stop_ip_entry.config(background="white")
        # start scan
        if not start == "" and not stop == "":
            scanner.start_ipv4_scan(start, stop)
            self.ipv4_scan_button.config(text="SCANNING\nStop Scan",
                command=self.scan_stop)
        self.update_results()

    def scan_ipv6(self):
        """start a ipv6 scan"""
        scanner.start_ipv6_scan("")
        self.ipv6_scan_button.config(text="Stop Scan",
            command=self.scan_stop)

    def scan_stop(self):
        settings.scanner_running = False
        self.ipv4_scan_button.config(text="Start Scan",
            command=self.scan_ipv4)
        self.ipv6_scan_button.config(text="Start Scan",
            command=self.scan_ipv6)

    def add_preset(self):
        """add input values into new preset"""
        pass

    def delete_preset(self):
        """add input values into new preset"""
        pass

    def load_preset(self):
        """add input values into new preset"""
        pass

    def update_results(self):
        """update the results list"""
        if settings.scanner_running:
            # add found nodes to resultlist
            offset_y = 38  # offset for the header
            for node in settings.scanner_scan_result:
                item_selected = IntVar()
                item_address = StringVar()
                item_name = StringVar()
                item_parents = StringVar()

                self.results_selector = Checkbutton(self.results, text="",
                    variable=item_selected, pady=2, padx=2, bg="#EEEEEE",
                    bd=0)
                self.results.create_window(6, offset_y + 8,
                    window=self.results_selector, anchor=NW)

                self.results_address_entry = Entry(self.results, width=14,
                    textvariable=item_address)
                self.results.create_window(39, offset_y + 9,
                    window=self.results_address_entry, anchor=NW)

                self.results_name_entry = Entry(self.results, width=15,
                    textvariable=item_name)
                self.results.create_window(166, offset_y + 9,
                    window=self.results_name_entry, anchor=NW)

                self.results_parents_entry = Entry(self.results, width=14,
                    textvariable=item_parents)
                self.results.create_window(301, offset_y + 9,
                    window=self.results_parents_entry,
                    anchor=NW)

                self.results_add_node_button = Button(self.results, text="+",
                    padx=20)
                self.results.create_window(427, offset_y + 4,
                    window=self.results_add_node_button, anchor=NW)

                item_address.set(str(node))

                offset_y = offset_y + 38
                self.results.create_line(0, offset_y, 490, offset_y, width=2)

            # update list every second
            self.window.after(2000, self.update_results)
        else:
            self.scan_stop()  # reset buttons