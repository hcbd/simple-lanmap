# -*- coding: utf-8 -*-

# Main GUI for lanmap

import settings
import log
import nodes
import monitor
from gui_scanner import scanner_gui
from gui_log import log_gui
from gui_editor import editor_gui
from tkinter import *
from tkinter import filedialog


class main_window(Frame):

    def __init__(self, main_gui=None):
        """set a reference and init the main window"""
        Frame.__init__(self, main_gui)
        self.main_gui = main_gui
        self.init_window()

    def init_window(self):
        """properties of the main_gui window"""
        # Window title
        self.main_gui.title(settings.program_name + " " + settings.program_version)

        # Create main layout frames and layout
        self.toolbar_frame = Frame(self.main_gui, height=25, bd=1)
        self.nodelist_frame = Frame(self.main_gui, bd=1, relief=SUNKEN)
        self.nodemap_frame = Frame(self.main_gui, bd=1, relief=SUNKEN)
        self.statusbar_frame = Frame(self.main_gui, height=20, bd=1)

        self.toolbar_frame.pack(side=TOP, fill=X, padx=5, ipadx=30, ipady=5)
        self.statusbar_frame.pack(side=BOTTOM, fill=X, ipadx=30, ipady=2)
        self.nodelist_frame.pack(side=LEFT, fill=Y)
        self.nodemap_frame.pack(side=RIGHT, fill=BOTH, expand=True, ipadx=15)

        # Create toolbar objects and layout
        self.monitor_button = Button(self.toolbar_frame, text="Start \nMonitor",
            command=lambda: self.start_monitor())
        self.monitor_button.pack(side=LEFT, fill=Y, pady=2, ipadx=15)

        self.save_nodes_button = Button(self.toolbar_frame, text="Save\nNetwork",
            command=self.save_nodes)
        self.save_nodes_button.pack(side=LEFT, fill=Y, pady=2, ipadx=15)

        self.load_nodes_button = Button(self.toolbar_frame, text="Load\nNetwork",
            command=self.load_nodes)
        self.load_nodes_button.pack(side=LEFT, fill=Y, pady=2, ipadx=15)

        self.edit_nodes_button = Button(self.toolbar_frame, text="Edit\nNodes")
        self.edit_nodes_button.pack(side=LEFT, fill=Y, pady=2, ipadx=15)
        self.edit_nodes_button.bind("<Button-1>", self.open_node_editor)

        self.scanner_button = Button(self.toolbar_frame, text="Network\nScanner")
        self.scanner_button.pack(side=LEFT, fill=Y, pady=2, ipadx=11)
        self.scanner_button.bind("<Button-1>", self.open_scanner)

        self.open_log_button = Button(self.toolbar_frame, text="Open Log",
            command=self.open_log)
        self.open_log_button.pack(side=RIGHT, fill=Y, pady=2, ipadx=8)
        #self.open_log_button.bind("<Button-1>", self.open_log)

        self.open_settings_button = Button(self.toolbar_frame, text="Settings")
        self.open_settings_button.pack(side=RIGHT, fill=Y, pady=2, ipadx=8)
        self.open_settings_button.bind("<Button-1>", self.open_settings)

        self.bg_image_button = Button(self.toolbar_frame, text="Clear\nBackground",
            command=self.change_image)
        self.bg_image_button.pack(side=RIGHT, fill=Y, pady=2, ipadx=6)
        if settings.gui_map_backgroundimage == "":
            self.bg_image_button.config(text="Load\nBackground")
            self.bg_image_button_state = 0

        # Create nodelist and layout
        self.nodelist = Canvas(self.nodelist_frame,
            background=settings.gui_list_backgroundcolor,
            width=settings.gui_list_width)
        self.nodelist_scrollbar = Scrollbar(self.nodelist_frame,
            orient="vertical", command=self.nodelist.yview)
        self.nodelist_scrollbar.pack(side=RIGHT, fill=Y)
        self.nodelist.configure(yscrollcommand=self.nodelist_scrollbar.set)
        self.nodelist.pack(side=LEFT, fill=BOTH, expand=True)
        self.update_nodelist()

        # Create nodemap and layout
        self.nodemap = Canvas(self.nodemap_frame,
            background=settings.gui_map_backgroundcolor,
            scrollregion=(0, 0, settings.gui_map_canvas_width,
            settings.gui_map_canvas_height))
        self.nodemap_scrollbar_x = Scrollbar(self.nodemap_frame, orient=HORIZONTAL)
        self.nodemap_scrollbar_y = Scrollbar(self.nodemap_frame, orient=VERTICAL)
        self.nodemap_scrollbar_y.pack(side=RIGHT, fill=Y)
        self.nodemap_scrollbar_y.config(command=self.nodemap.yview)
        self.nodemap_scrollbar_x.pack(side=BOTTOM, fill=X)
        self.nodemap_scrollbar_x.config(command=self.nodemap.xview)
        self.nodemap.config(xscrollcommand=self.nodemap_scrollbar_x.set,
            yscrollcommand=self.nodemap_scrollbar_y.set)
        self.nodemap.pack(side=TOP, fill=BOTH, expand=True)
        self.nodemap_width = self.nodemap.winfo_reqwidth()
        self.nodemap_height = self.nodemap.winfo_reqheight()
        self.nodemap.bind("<Configure>", self.resize_map)
        self.nodemap.bind("<B1-Motion>", self.move_node)
        self.nodemap.bind("<ButtonRelease-1>", self.move_node_update)
        self.update_nodemap()

        # Statusbar and layout
        self.statusbar_text = StringVar()
        self.statusbar_text.set("Lanmap")
        self.statusbar_node_status = StringVar()
        self.statusbar_node_status.set("0 of 0 Nodes Online")
        self.statusbar_label1 = Label(self.statusbar_frame,
            textvariable=self.statusbar_text).pack(side=LEFT, padx=3)
        self.statusbar_label2 = Label(self.statusbar_frame,
            textvariable=self.statusbar_node_status).pack(side=RIGHT, padx=3)

    # Toolbar funtions
    def start_monitor(self):
        """runs when the start monitor button is pressed on the toolbar"""
        self.monitor_button.config(text="Stop\nmonitor",
            command=lambda: self.stop_monitor())
        monitor.start()
        self.update_nodemap()
        self.update_nodelist()
        self.update_monitor()

    def stop_monitor(self):
        """stops the monitor when the start/stop monitor buttion is
           pressed on the toolbar"""
        self.monitor_button.config(text="Start\nmonitor",
            command=lambda: self.start_monitor())
        monitor.stop()
        self.update_nodemap()
        self.update_nodelist()

    def update_monitor(self):
        """reload the map every x seconds to update GUI"""
        if settings.monitor_running:
            self.update_nodemap()
            self.update_nodelist()
            root.after(2000, self.update_monitor)

    def save_nodes(self):
        """runs when the save nodes button is pressed on the toolbar"""
        location = filedialog.asksaveasfilename(defaultextension=".nodes",
            filetypes=[('Node File', '.nodes'), ('Text File', '.txt')],
            title='Save Nodes to File', initialfile='my-network.nodes')
        nodes.save_to_disk(location)

    def load_nodes(self):
        """runs when the load nodes button is pressed on the toolbar"""
        location = filedialog.askopenfilename(defaultextension=".nodes",
            filetypes=[('Node File', '.nodes'), ('Text File', '.txt')],
            title='Save Nodes to File')
        nodes.load_from_disk(location)
        self.update_nodelist()
        self.update_nodemap()

    def open_node_editor(self, event):
        """runs when the edit nodes button is pressed on the toolbar"""
        self.editor_window = editor_gui()
        self.editor_window.show()
        pass

    def open_scanner(self, event):
        """runs when the network scanner button is pressed on the toolbar"""
        self.scanner_window = scanner_gui()
        self.scanner_window.show()

    def change_image(self, event=0):
        """Load or Clear the Background image on the map"""
        if settings.gui_map_backgroundimage == "":
            #load path and image
            openf = filedialog.askopenfilename(defaultextension=".gif",
                filetypes=[('GIF files', '.gif'), ('all files', '.*')],
                title="Select Background Image - GIF files only")
            if openf:
                settings.gui_map_backgroundimage = openf
        else:
            #clear background
            settings.gui_map_backgroundimage = ""
        self.update_nodemap()

    def open_log(self):
        """runs when the open log button is pressed on the toolbar"""
        self.log_window = log_gui()
        self.log_window.show()

    def open_settings(self, event):
        """runs when the settings button is pressed on the toolbar"""
        pass

    # Nodelist functions
    def update_nodelist(self):
        """draws a header and all the nodes on to the nodelist canvas"""
        self.nodelist.delete(ALL)
        self.nodelist.create_rectangle(2, 2, settings.gui_list_width, 26,
            fill=settings.gui_list_header_bgcolor)
        self.nodelist.create_text(23, 15, text="Network Nodes", anchor=W,
            fill=settings.gui_list_header_text_color)
        highlight_switch = False
        counter = 0
            # list and display each node from the nodelist
        for node in nodes.nodelist:
            if not settings.gui_list_show_nostatus_nodes:
                if not node.check_status:
                    continue
            number = counter + 1
            name = str(number) + ". " + str(node.name)
            if node.check_status:
                if len(node.ipv4) == 0 and len(node.ipv6) == 1:
                    address = "[" + str(node.ipv6[0]) + "]"
                else:
                    address = "[" + str(node.ipv4[0]) + "]"
            else:
                address = "[non-pingable device]"
            pos_top = number * 38 - 11
            pos_bottom = pos_top + 38
            pos_text = pos_top + 12
            status_color = "#FFFFFF"
            text_color = "#000000"
            if settings.monitor_running:
                if node.status == "online":
                    status_color = settings.gui_list_online_status_color
                    text_color = settings.gui_list_online_status_text_color
                elif node.status == "awaiting":
                    status_color = settings.gui_list_awaiting_status_color
                    text_color = settings.gui_list_awaiting_status_text_color
                elif node.status == "offline":
                    status_color = settings.gui_list_offline_status_color
                    text_color = settings.gui_list_offline_status_text_color
                else:
                    status_color = settings.gui_list_nostatus_color
                    text_color = settings.gui_list_nostatus_text_color
            else:
                if highlight_switch:
                    status_color = settings.gui_list_odd_color
                    highlight_switch = False
                else:
                    status_color = settings.gui_list_even_color
                    highlight_switch = True
            self.nodelist.create_rectangle(2, pos_top, settings.gui_list_width,
                    pos_bottom, fill=status_color, tags=address)
            self.nodelist.create_text(6, pos_text, text=name,
                fill=text_color, anchor=W, tags=address)
            self.nodelist.create_text(21, (pos_text + 15), text=address,
                fill=text_color, anchor=W, tags=address)
            counter = counter + 1

    # Nodemap functions
    def update_nodemap(self):
        """update the map view"""
        self.nodemap.delete(ALL)
        self.update_nodemap_nodes()
        self.update_statusbar()

    def update_nodemap_bgimage(self):
        """reloads the background image on the nodemap"""
        if settings.gui_map_backgroundimage == "":
            self.bg_image_button.config(text="Load\nBackground")
            return
        bgimage = PhotoImage(file=settings.gui_map_backgroundimage)
        self.nodemap.image = bgimage
        self.nodemap.create_image(0, 0, image=bgimage, anchor=NW,
            tags="bg")
        self.bg_image_button.config(text="Clear\nBackground")

    def update_nodemap_nodes(self):
        """reloads the nodes on the nodemap"""
        global node
        self.nodemap.delete(ALL)
        self.update_nodemap_bgimage()
        no_coord_count = 0
        for node in nodes.nodelist:
            # set and calculate all necessary vars
            name = node.name
            status = node.status
            node_size = settings.gui_map_node_size
            if node.coordinates == '':
                node_pos_x = 50
                node_pos_y = 50 * no_coord_count + 30
                no_coord_count = no_coord_count + 1
            else:
                coords = node.coordinates.split("x")
                if coords[0] and coords[1]:
                    node_pos_x = coords[0]
                    node_pos_y = coords[1]
                else:
                    node_pos_x = 50
                    node_pos_y = 50 * no_coord_count + 30
                    no_coord_count = no_coord_count + 1
            node.coordinates = str(node_pos_x) + "x" + str(node_pos_y)
            node_pos_x2 = int(float(node_pos_x)) + node_size
            node_pos_y2 = int(float(node_pos_y)) + node_size
            node_circle_border = settings.gui_map_nodecircle_bordersize

            # set node colors
            if settings.monitor_running:
                if status == "online":
                    node_color = settings.gui_map_node_online_status_color
                    text_color = settings.gui_map_node_online_status_text_color
                elif status == "awaiting":
                    node_color = settings.gui_map_node_awaiting_status_color
                    text_color = settings.gui_map_node_awaiting_status_text_color
                elif status == "offline":
                    node_color = settings.gui_map_node_offline_status_color
                    text_color = settings.gui_map_node_offline_status_text_color
                else:
                    node_color = settings.gui_map_node_nostatus_color
                    text_color = settings.gui_map_node_nostatus_text_color
            else:
                node_color = settings.gui_map_node_nostatus_color
                text_color = settings.gui_map_node_nostatus_text_color

            # Place nodes on nodemap
            self.nodemap.create_oval(node_pos_x, node_pos_y, node_pos_x2, node_pos_y2,
                fill=node_color, activefill=settings.gui_map_node_onmouseover_color,
                outline="#222222", width=node_circle_border,
                tags=("node", "top", name))
            if settings.gui_map_node_show_label:
                x = int(float(node_pos_x)) + settings.gui_map_node_size + 3
                y = int(float(node_pos_y)) + 2
                node_text = self.nodemap.create_text(x, y, text=name, anchor=NW,
                    fill=text_color, tags=("node", "top"))
                node_text_coords = self.nodemap.bbox(node_text)
                self.nodemap.create_rectangle(node_text_coords[0] - node_size / 2,
                    node_text_coords[1] - 1, node_text_coords[2] + 2,
                    node_text_coords[3], width=1, fill=node_color,
                    tags=("middle", "node", ))

            # draw lines to parents
            if not settings.gui_map_show_lines_to_parent:
                continue
                # loop thru all nodes and find a ipv4 match
            for parent_ip in node.parents:
                if parent_ip == "":
                    continue
                for test_node in nodes.nodelist:
                    for test_ip in test_node.ipv4:
                        if not test_ip == parent_ip:
                            continue
                        start_x = int(float(node_pos_x)) + node_size / 2
                        start_y = int(float(node_pos_y)) + node_size / 2
                        xy = test_node.coordinates.split("x")
                        stop_x = int(float(xy[0])) + node_size / 2
                        stop_y = int(float(xy[1])) + node_size / 2
                        if node.wireless_to_parent:
                            self.nodemap.create_line(start_x, start_y,
                                stop_x, stop_y, fill="white",
                                width=3, tags=("subline"))
                            self.nodemap.create_line(start_x, start_y,
                                stop_x, stop_y, fill=settings.gui_map_line_color,
                                width=3, tags=("line"), smooth=True, dash=(9, 7))
                        else:
                            self.nodemap.create_line(start_x, start_y,
                                stop_x, stop_y, fill=settings.gui_map_line_color,
                                width=3, tags=("line"))
        self.reset_layers()

    def resize_map(self, event):
        """if a window/canvas resize event happens, update map"""
        # get scale

        # resize canvas
        self.nodemap_width = event.width
        self.nodemap_height = event.height
        self.nodemap.config(width=self.nodemap_width, height=self.nodemap_height)
        settings.gui_map_canvas_height = self.nodemap_height
        settings.gui_map_canvas_width = self.nodemap_width

        # reset layering
        self.reset_layers()

    def reset_layers(self):
        """set the correct layer index"""
        self.nodemap.tag_lower("bg")
        self.nodemap.tag_raise("line")
        self.nodemap.tag_raise("middle")
        self.nodemap.tag_raise("top")

    def move_node(self, event):
        """move node around map, with click and hold"""
        if settings.monitor_running:
            return
        canvas = event.widget
        x = canvas.canvasx(event.x)
        y = canvas.canvasy(event.y)
        node_coords = canvas.coords(CURRENT)
        try:
            offset_x = x - int(node_coords[0] + settings.gui_map_node_size / 2)
            offset_y = y - int(node_coords[1] + settings.gui_map_node_size / 2)
            for tag in canvas.gettags(CURRENT):
                for node in nodes.nodelist:
                    if not tag == node.name:
                        continue
                    canvas.move(CURRENT, offset_x, offset_y)
                    max_x = settings.gui_map_canvas_width
                    max_y = settings.gui_map_canvas_height
                    if x < 0 or x > max_x or y < 0 or y > max_y:
                        continue
                    coords = str(int(x - offset_x) - settings.gui_map_node_size / 2)
                    coords += "x"
                    coords += str(int(y - offset_y) - settings.gui_map_node_size / 2)
                    node.coordinates = coords
        except:
            pass  # ignore errors

    def move_node_update(self, event):
        self.update_nodemap()

    # Statusbar functions
    def update_statusbar(self):
        """update all components on the statusbar"""
        online_nodes = 0
        total_nodes = 0
        for node_x in nodes.nodelist:
            if node_x.status == "online":
                online_nodes = online_nodes + 1
            if node_x.check_status:
                total_nodes = total_nodes + 1
        node_status = str(online_nodes) + " of " + str(total_nodes)
        node_status += " Nodes Online"
        # these give an attributeError... but why?
        #self.statusbar_node_status.set(node_status)
        #self.statusbar_text.set(log.last())


# Main Program Loop


def saveAndQuit():
    #settings.save()
    nodes.save_to_disk()
    #log.save()
    root.destroy()

# main instance
root = Tk()

log.add("Lanmap ready")
#settings.load()

# save config if window is closed
root.protocol("WM_DELETE_WINDOW", saveAndQuit)

root.geometry(settings.gui_window_size)
#root.attributes('-zoomed', True) #start with maximized gui

app = main_window(root)
root.mainloop()