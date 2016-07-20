# -*- coding: utf-8 -*-

# Containing all the functions for nodes control


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
        self.parents = ''
        self.wireless_to_parent = False
        self.coordinates = '50x50'


def save_to_disk():
    """Save the current nodelist to a .nodes file"""
    #TODO
    pass


def load_from_disk():
    """Load a *.nodes file from disk and import the nodes in
       to the nodelist"""
    #TODO
    pass


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
    client1.ipv4 = ['172.16.32.32', ]
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

#TODO: check for saved version first

load_example_nodelist()