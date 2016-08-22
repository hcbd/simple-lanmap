# -*- coding: utf-8 -*-


# build the log window
import settings
from tkinter import *
import log


# log GUI
class log_gui(object):
    def __init__(self):
        pass

    def show(self):
        """show the log window"""
        if not settings.gui_log_open:
            settings.gui_log_open = True
            self.build_window()

    def close(self):
        """close the log window"""
        self.window.destroy()
        settings.gui_log_open = False

    def build_window(self):
        """build main log window"""
        self.window = Toplevel()
        self.window.title("Lanmap - Log")
        self.window.protocol("WM_DELETE_WINDOW", self.close)

        # frames/layout
        self.top_frame = Frame(self.window)
        self.bottom_frame = Frame(self.window)
        self.top_frame.pack(side=TOP, fill=BOTH, expand=1)
        self.bottom_frame.pack(side=BOTTOM, fill=X)

        self.log = Listbox(self.top_frame, width=110, height=26, bd=2)
        self.log.pack(side=TOP)
        for n in log.log:
            self.log.insert(END, " " + n)

        self.log_clear_button = Button(self.bottom_frame, text="Clear Log",
            command=self.clear_log)
        self.log_clear_button.pack(side=LEFT, padx=5, pady=3, fill=X)

        self.log_save_button = Button(self.bottom_frame, text="Save Log",
            state=DISABLED)
        self.log_save_button.pack(side=RIGHT, padx=5, pady=3, fill=X)

    def refresh_log(self):
        self.log.delete(0, END)
        for n in log.log:
            self.log.insert(END, " " + n)

    def clear_log(self):
        log.log = []
        self.refresh_log()

    def save_log(self):
        #TODO
        pass