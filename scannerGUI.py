# -*- coding: utf-8 -*-

# build the scanner window
import settings
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
        self.window.destroy()
        settings.gui_scanner_window_open = False

    def build_window(self):
        self.window = Toplevel()
        self.window.title("Lanmap - Network Scanner")
        self.window.geometry("700x500")
        self.window.protocol("WM_DELETE_WINDOW", self.close)

        # 2 frames and layout

        # Select mode buttons
        self.selected_scan_mode = IntVar()
        self.select_ipv4_scan = Radiobutton(self.window, text="IPv4 Scan",
            variable=self.selected_scan_mode, value=0, indicatoron=0,
            height=2, padx=15)
        self.select_ipv4_scan.grid(row=0, column=0, pady=4)

        self.select_ipv6_scan = Radiobutton(self.window, text="IPv6 Scan",
            variable=self.selected_scan_mode, value=1, indicatoron=0,
            height=2, padx=15)
        self.select_ipv6_scan.grid(row=0, column=1)
        self.select_ipv4_scan.bind("<Button-1>", self.switch_to_ipv4)
        self.select_ipv6_scan.bind("<Button-1>", self.switch_to_ipv6)
        #TODO
        # IPv4 scan settings
        #self.ipv4_titel = Label(text="IPv4 Scan Settings")
        #self.preset_selector = ''
        #self.load_preset_button = Button(text="Load Preset")

        # IPv6 scan settings

    def scan_ipv4(self, event):
        """start a ipv4 scan"""
        pass

    def scan_ipv6(self, event):
        """start a ipv6 scan"""
        pass

    def switch_to_ipv4(self, event):
        """if the ipv4 scan button is pressed, adjust tkinter widgets"""

    def switch_to_ipv6(self, event):
        """if the ipv6 scan button is pressed, adjust tkinter widgets"""
        pass