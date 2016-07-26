# -*- coding: utf-8 -*-

# all the settings for lanmap go here

import configparser
import log


# 1. general program settings
program_name = 'Lanmap'
program_version = 'Version 0.3.0'
program_settingsfile = 'config.ini'
program_last_used_nodesfile = 'nodes.ini'
program_computer_addresses = []
program_computer_interfaces = []

# 2. monitor settings
monitor_running = False
monitor_interval = 10     # in seconds
monitor_ping_count = 1    # in seconds
monitor_ping_timeout = 1  # amount of pings send to node

# 3. scanner settings
scanner_running = False
scanner_scan_result = []
scanner_preset_file = 'scan-presets.ini'
scanner_presets = []

# 4. gui settings
gui_window_size = "1180x760"
gui_scanner_window_open = False

# 4.1 gui - node list settings
gui_list_width = 190
gui_list_backgroundcolor = "#7A7A7A"
gui_list_header_bgcolor = "#BBBBBB"
gui_list_header_text_color = "#000000"
gui_list_online_status_color = "#00FF15"
gui_list_online_status_text_color = "#000000"
gui_list_awaiting_status_color = "#FF8400"
gui_list_awaiting_status_text_color = "#000000"
gui_list_offline_status_color = "#FF2626"
gui_list_offline_status_text_color = "#000000"
gui_list_nostatus_color = "#DDDDDD"
gui_list_nostatus_text_color = "#000000"
gui_list_even_color = "#FFFFFF"
gui_list_odd_color = "#DDDDDD"
gui_list_show_nostatus_nodes = True

# 4.2 gui - node map settings
gui_map_canvas_height = 1200
gui_map_canvas_width = 1500
gui_map_backgroundimage = ""
gui_map_backgroundcolor = "#7A7A7A"
gui_map_text_color = "#000000"
gui_map_node_size = 17
gui_map_nodecircle_bordersize = 2
gui_map_node_show_label = True
gui_map_show_lines_to_parent = True
gui_map_line_color = "#000000"
gui_map_node_online_status_color = "#00FF15"
gui_map_node_online_status_text_color = "#000000"
gui_map_node_awaiting_status_color = "#FF8400"
gui_map_node_awaiting_status_text_color = "#000000"
gui_map_node_offline_status_color = "#FF2626"
gui_map_node_offline_status_text_color = "#FFFFFF"
gui_map_node_nostatus_color = "#FFFFFF"
gui_map_node_nostatus_text_color = "#000000"
gui_map_node_onmouseover_color = "#555555"


# 5. log settings
log_enabled = True
log_timestamp_enabled = True


def load():
    """Loads the settings from the settings file on disk
       if no file then defaults are loaded"""
    try:
        config = configparser.ConfigParser()
        config.read(program_settingsfile)

        #TODO: get/proces all settings from file ini file

        log.add('Loaded the settings from ' + program_settingsfile)

    except:
        logmsg = 'Error loading the settings from '
        logmsg += program_settingsfile
        logmsg += ', using default settings'
        log.add(logmsg)


def save():
    """Save all current settings to a settingsfile on disk"""
    #TODO
    pass