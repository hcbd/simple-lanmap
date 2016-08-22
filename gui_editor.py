# -*- coding: utf-8 -*-

import settings
import nodes
from tkinter import *


# Node Editor GUI
class editor_gui(object):
    def __init__(self):
        pass

    def show(self):
        """show the node editor window"""
        if not settings.gui_editor_open:
            settings.gui_editor_open = True
            self.build_window()

    def close(self):
        """close the log window"""
        self.window.destroy()
        settings.gui_editor_open = False

    def build_window(self):
        self.window = Toplevel()
        self.window.title("Lanmap - Node Editor")
        self.window.protocol("WM_DELETE_WINDOW", self.close)

        # Frames / Layout
        self.headerlabel = Label(self.window,
            text="SELECT NODE FROM LIST")
        self.headerlabel.pack(side=TOP, fill=X, padx=4, pady=7, expand=1)
        self.left_frame = Frame(self.window)
        self.right_frame = Frame(self.window, bd=3)
        self.left_frame.pack(side=LEFT, fill=Y, anchor=N, padx=10, pady=10)
        self.right_frame.pack(side=RIGHT, fill=BOTH, expand=1, padx=5, pady=5)

        # Listbox with Nodes
        self.listbox = Listbox(self.left_frame, width=20, bd=2)
        self.listbox.pack(side=TOP, fill=X, expand=1, anchor=N)

        # only buttonrelease works, because the selection in the listbox
        # is done after button click action and before the button
        # release action.
        self.listbox.bind("<ButtonRelease-1>", self.load_node)

        self.listbox.insert(END, " [NEW NODE]")
        for n in nodes.nodelist:
            self.listbox.insert(END, " " + n.name)

        # Selected Node edit area
        self.node_name = StringVar()
        self.node_ipv4 = StringVar()
        self.node_ipv6 = StringVar()
        self.node_ipv6_linklocal = StringVar()
        self.hostname = StringVar()
        self.url = StringVar()
        self.check_status = StringVar()
        self.parents = StringVar()
        self.wireless_to_parent = StringVar()

        frame1 = Frame(self.right_frame)
        frame1.pack(side=TOP, fill=X, padx=4, pady=4)
        self.namelabel = Label(frame1, text="Name: ")
        self.namelabel.pack(side=LEFT, anchor=E)
        self.name_entry = Entry(frame1, textvariable=self.node_name,
            width=22)
        self.name_entry.pack(side=RIGHT, anchor=W, padx=3)

        frame2 = Frame(self.right_frame)
        frame2.pack(side=TOP, fill=X, padx=4, pady=4)
        self.ipv4label = Label(frame2, text="IPv4 addresses: ")
        self.ipv4label.pack(side=LEFT, anchor=E)
        self.ipv4_entry = Entry(frame2, textvariable=self.node_ipv4,
            width=22)
        self.ipv4_entry.pack(side=RIGHT, anchor=W, padx=3)

        frame3 = Frame(self.right_frame)
        frame3.pack(side=TOP, fill=X, padx=4, pady=4)
        self.ipv6label = Label(frame3, text="IPv6 addresses: ")
        self.ipv6label.pack(side=LEFT, anchor=E)
        self.ipv6_entry = Entry(frame3, textvariable=self.node_ipv6,
            width=22)
        self.ipv6_entry.pack(side=RIGHT, anchor=W, padx=3)

        frame4 = Frame(self.right_frame)
        frame4.pack(side=TOP, fill=X, padx=4, pady=4)
        self.ipv6lklabel = Label(frame4, text="IPv6 link local: ")
        self.ipv6lklabel.pack(side=LEFT, anchor=E)
        self.ipv6lk_entry = Entry(frame4, textvariable=self.node_ipv6_linklocal,
            width=22)
        self.ipv6lk_entry.pack(side=RIGHT, anchor=W, padx=3)

        frame5 = Frame(self.right_frame)
        frame5.pack(side=TOP, fill=X, padx=4, pady=4)
        self.hostnamelabel = Label(frame5, text="Hostname: ")
        self.hostnamelabel.pack(side=LEFT, anchor=E)
        self.hostname_entry = Entry(frame5, textvariable=self.hostname,
            width=22)
        self.hostname_entry.pack(side=RIGHT, anchor=W, padx=3)

        frame6 = Frame(self.right_frame)
        frame6.pack(side=TOP, fill=X, padx=4, pady=4)
        self.urllabel = Label(frame6, text="Web admin url: ")
        self.urllabel.pack(side=LEFT, anchor=E)
        self.url_entry = Entry(frame6, textvariable=self.url,
            width=22)
        self.url_entry.pack(side=RIGHT, anchor=W, padx=3)

        frame7 = Frame(self.right_frame)
        frame7.pack(side=TOP, fill=X, padx=4, pady=4)
        self.check_statuslabel = Label(frame7, text="Ping Node:       ")
        self.check_statuslabel.pack(side=LEFT, anchor=E)
        self.check_status_entry = Checkbutton(frame7,
            textvariable=self.check_status)
        self.check_status_entry.pack(side=LEFT, anchor=E, padx=3)

        frame8 = Frame(self.right_frame)
        frame8.pack(side=TOP, fill=X, padx=4, pady=4)
        self.parentslabel = Label(frame8, text="Parent Nodes: ")
        self.parentslabel.pack(side=LEFT, anchor=E)
        self.parents_entry = Entry(frame8, textvariable=self.parents,
            width=22)
        self.parents_entry.pack(side=RIGHT, anchor=W, padx=3)

        frame9 = Frame(self.right_frame)
        frame9.pack(side=TOP, fill=X, padx=4, pady=4)
        self.wireless_to_parentlabel = Label(frame9,
            text="Connects wireless to parent: ")
        self.wireless_to_parentlabel.pack(side=LEFT, anchor=E)
        self.wireless_to_parent_entry = Checkbutton(frame9,
            textvariable=self.wireless_to_parent)
        self.wireless_to_parent_entry.pack(side=LEFT, anchor=E, padx=3)

        frame10 = Frame(self.right_frame)
        frame10.pack(side=TOP, fill=X, padx=4, pady=5)

    def load_node(self, event):
        """load selected node values into the edit fields"""
        nr = self.listbox.curselection()[0]
        if not int(nr) == 0:
            self.node_name.set(nodes.nodelist[int(nr) - 1].name)
            self.node_ipv4.set(nodes.nodelist[int(nr) - 1].ipv4)
            self.node_ipv6.set(nodes.nodelist[int(nr) - 1].ipv6)
            self.node_ipv6_linklocal.set(nodes.nodelist[int(nr) - 1].ipv6_linklocal)
            self.hostname.set(nodes.nodelist[int(nr) - 1].hostname)
            self.url.set(nodes.nodelist[int(nr) - 1].url)
            self.check_status.set(nodes.nodelist[int(nr) - 1].check_status)
            self.parents.set(nodes.nodelist[int(nr) - 1].parents)
            self.wireless_to_parent.set(nodes.nodelist[int(nr) - 1].wireless_to_parent)
        else:
            pass

        pass