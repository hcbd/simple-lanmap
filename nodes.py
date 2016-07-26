# -*- coding: utf-8 -*-

# Containing all the functions for nodes control
import settings
import configparser
import log


class node(object):

    def __init__(self):
        """Create all properties of a network node"""
        self.name = 'Unnamed Node'
        self.ipv4 = ['0.0.0.0', ]
        self.ipv6 = ['2001:0000:0000:0000:0000:0000:0000:0001', ]
        self.ipv6_linklocal = 'fe80:0000:0000:0000:0000:0000:0000:0001'
        self.hostname = 'sub.domain.local'
        self.url = 'http://0.0.0.0'
        self.check_status = True
        self.status = 'offline'
        self.parents = []
        self.wireless_to_parent = False
        self.coordinates = '50x50'


def save_to_disk(nodefile=settings.program_last_used_nodesfile):
    """Save the current nodelist to a .nodes file"""
    try:
        f = open(nodefile, "w")
        f.write("\n")
        f.write("# Lanmap Nodes\n")
        f.write("\n")
        f.write("[Map Background]\n")
        imgloc = settings.gui_map_backgroundimage
        f.write("image location=" + imgloc + "\n")
        f.write("\n")
        x = 1
        for node in nodelist:
            f.write("[Node " + str(x) + "]\n")
            f.write("name=" + str(node.name) + "\n")
            f.write("ipv4=" + str(node.ipv4) + "\n")
            f.write("ipv6=" + str(node.ipv6) + "\n")
            f.write("ipv6 linklocal=" + str(node.ipv6_linklocal) + "\n")
            f.write("hostname=" + str(node.hostname) + "\n")
            f.write("url=" + str(node.url) + "\n")
            f.write("check status=" + str(node.check_status) + "\n")
            f.write("status=" + str(node.status) + "\n")
            f.write("parents=" + str(node.parents) + "\n")
            f.write("wireless to parent=" + str(node.wireless_to_parent) + "\n")
            f.write("coordinates=" + str(node.coordinates) + "\n")
            f.write("\n")
            x = x + 1
    except:
        print("error writing to nodes file")
    pass


def load_from_disk(nodefile=settings.program_last_used_nodesfile):
    """Load a *.nodes file from disk and import the nodes in
       to the nodelist"""
    global nodelist
    nodelist = []
    data = ""
    try:
        f = open(nodefile, "r")
        data = f.read()
    except:
        print("error loading file")
        load_example_nodelist()
        log.add("error reading nodes file, reverting back to example list")

    parser = configparser.ConfigParser()
    parser.read_string(data)
    try:
        settings.gui_map_backgroundimage = parser['Map Background']['image location']
    except:
        settings.gui_map_backgroundimage = ""
    x = 1
    while True:
        nodef = False
        try:
            nodef = "Node " + str(x)
            a = parser[nodef]['name']
        except:
            break
        if not nodef:
            break
        name = parser[nodef]['name']
        ipv4 = parser[nodef]['ipv4']
        addr = ipv4.split(", ")
        ipv4 = []
        for ip in addr:
            ip = ip.replace("[", "")
            ip = ip.replace("]", "")
            ip = ip.replace("\'", "")
            ip = ip.replace("\"]", "")
            ip = ip.replace(" ", "")
            ip = ip.replace(",", "")
            ipv4.append(ip)
        ipv6 = parser[nodef]['ipv6']
        addr = ipv6.split(", ")
        ipv6 = []
        for ip in addr:
            ip = ip.replace("[", "")
            ip = ip.replace("]", "")
            ip = ip.replace("\'", "")
            ip = ip.replace("\"]", "")
            ip = ip.replace(" ", "")
            ip = ip.replace(",", "")
            ipv6.append(ip)
        ipv6_linklocal = parser[nodef]['ipv6 linklocal']
        hostname = parser[nodef]['hostname']
        url = parser[nodef]['url']
        check_status = parser[nodef]['check status']
        status = parser[nodef]['status']
        parents = parser[nodef]['parents']
        addr = parents.split(", ")
        parents = []
        for ip in addr:
            ip = ip.replace("[", "")
            ip = ip.replace("]", "")
            ip = ip.replace("\'", "")
            ip = ip.replace("\"]", "")
            ip = ip.replace(" ", "")
            ip = ip.replace(",", "")
            parents.append(ip)
        wireless_to_parent = parser[nodef]['wireless to parent']
        coordinates = parser[nodef]['coordinates']
        # input node into nodelist
        new_node = node()
        new_node.name = name
        new_node.ipv4 = ipv4
        new_node.ipv6 = ipv6
        new_node.ipv6_linklocal = ipv6_linklocal
        new_node.hostname = hostname
        new_node.url = url
        new_node.status = ""
        if check_status == "True":
            check_status = True
        elif check_status == "False":
            check_status = False
        new_node.check_status = check_status
        if status == "True": status = True
        elif status == "False": status = False
        new_node.status = status
        new_node.parents = parents
        if wireless_to_parent == "True": wireless_to_parent = True
        elif wireless_to_parent == "False": wireless_to_parent = False
        new_node.wireless_to_parent = wireless_to_parent
        new_node.coordinates = coordinates
        nodelist.append(new_node)
        x = x + 1
    return True


def load_example_nodelist():
    """Load the example nodes in to the nodelist"""
    global nodelist
    # Node 1 - Modem/Wirelessrouter/Gateway
    router = node()
    router.name = 'Modem/Wirelessrouter'
    router.ipv4 = ['192.168.1.1', ]
    router.ipv6 = []
    router.ipv6_linklocal = 'fe80:0000:0000:0000:0000:0000:0000:0001'
    router.hostname = 'router.local'
    router.url = 'http://192.168.1.1'
    router.check_status = True
    router.status = 'offline'
    router.parents = ['', ]
    router.wireless_to_parent = False
    router.coordinates = '300x100'

    # Node 2 - Switch
    switch = node()
    switch.name = 'Switch'
    switch.ipv4 = ['192.168.1.2', ]
    switch.ipv6 = ['2001:0000:0000:0000:0000:0000:0000:0002', ]
    switch.ipv6_linklocal = 'fe80:0000:0000:0000:0000:0000:0000:0002'
    switch.hostname = 'switch.local'
    switch.url = 'http://192.168.1.2'
    switch.check_status = False
    switch.status = 'nostatus'
    switch.parents = ['192.168.1.1', ]
    switch.wireless_to_parent = False
    switch.coordinates = '225x200'

    # Node 3
    client1 = node()
    client1.name = 'File Server'
    client1.ipv4 = ['192.168.1.3', ]
    client1.ipv6 = []
    client1.ipv6_linklocal = 'fe80:0000:0000:0000:0000:0000:0000:0003'
    client1.hostname = 'feda-3ews'
    client1.url = ''
    client1.check_status = True
    client1.status = 'offline'
    client1.parents = ['192.168.1.2', ]
    client1.wireless_to_parent = False
    client1.coordinates = '150x300'

    # Node 4
    server = node()
    server.name = 'Backup Server'
    server.ipv4 = ['192.168.1.3', ]
    server.ipv6 = []
    server.ipv6_linklocal = 'fe80:0000:0000:0000:0000:0000:0000:0003'
    server.hostname = 'feda-3ews'
    server.url = ''
    server.check_status = True
    server.status = 'offline'
    server.parents = ['192.168.1.2', ]
    server.wireless_to_parent = False
    server.coordinates = '300x300'

    # Node 5 - Wifi Client 1
    client2 = node()
    client2.name = 'Wifi Client 1'
    client2.ipv4 = ['192.168.1.4', ]
    client2.ipv6 = ['2001:0000:0000:0000:0000:0000:0000:0004', ]
    client2.ipv6_linklocal = 'fe80:0000:0000:0000:0000:0000:0000:0004'
    client2.hostname = 'Smartphone'
    client2.url = ''
    client2.check_status = True
    client2.status = 'offline'
    client2.parents = ['192.168.1.1', ]
    client2.wireless_to_parent = True
    client2.coordinates = '375x200'

    # add nodes to the list
    nodelist.append(router)
    nodelist.append(switch)
    nodelist.append(client1)
    nodelist.append(server)
    nodelist.append(client2)

nodelist = []

load_from_disk()
#load_example_nodelist()