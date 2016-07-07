# -*- coding: utf-8 -*-

import log as logger

from configparser import ConfigParser, RawConfigParser, SafeConfigParser
from collections import OrderedDict

# DEFAULT SETTINGS

# Network settings
networkMyIp = "0.0.0.0"
networkGateway = "192.168.1.1"
networkDhcpServer = "192.168.1.1"
networkDnsServer = "192.168.1.1"
networkDhcpDetectRunning = False
networkFoundDhcpServers = []

# Scanner settings
scanStartAddress = "192.168.1.1"
scanStopAddress = "192.168.1.254"
scanPingTries = 1
scanPingTimeout = 1
scanGetHostnames = 0
scanRunning = False
scanNodes = [] # list to scan
scanFoundNodes = [] # found

# Monitor settings
monitorPingInterval = 30
monitorUpdateInterval = 15000
monitorPingTries = 1
monitorPingTimeout = 1000
monitorRunning = False

# Example Nodes / example config loaded when no settingsfile is found
nodesDefault = [["Wireless Router",                   #0 name
          "Router",                                   #1 group
          "Router",                                   #2 type of device
          "Uplink location",                          #3 location name
          True,                                       #4 reachable/pingable device
          "Awaiting",                                 #5 node status
         ["192.168.1.1",],                            #6 ipv4 address(es)
         ["2001:0000:0000:0000:0000:0000:0000:0001",],#7 ipv6 public address(es)
         "fe80::1",                                   #8 ipv6 link local address
         [1,],                                        #9 vlan id(s)
         ["",],                                       #10 parent(s) ip address
          0,                                          #11 monitorlist node position
          "344x57",                                   #12 LANmap position
          False,                                      #13 wireless connected to parent
          0,                                          #14 Canvas ID
          ""],                                        #15 icon (location)

          ["Wireless Client",                         #0 name
          "Client",                                   #1 group
          "Client",                                   #2 type of device
          "Uplink location",                          #3 location name
          True,                                       #4 reachable/pingable device
          "Awaiting",                                 #5 node status
         ["192.168.1.2",],                            #6 ipv4 address(es)
         ["2001:0000:0000:0000:0000:0000:0000:0002",],#7 ipv6 public address(es)
         "fe80::1",                                   #8 ipv6 link local address
         [1,],                                        #9 vlan id(s)
         ["192.168.1.1",],                            #10 parent(s) ip address
          1,                                          #11 monitorlist node position
          "538x295",                                  #12 LANmap position
          True,                                       #13 wireless connected to parent
          0,                                          #14 Canvas ID
          ""],                                        #15 icon (location)

          ["Dumb Switch",                             #0 name
          "Switch",                                   #1 group
          "Switch",                                   #2 type of device
          "Uplink location",                          #3 location name
          False,                                      #4 reachable/pingable device
          "",                                         #5 node status
         ["Dumbswitch",],                             #6 ipv4 address(es)
         ["2001:0000:0000:0000:0000:0000:0000:0003",],#7 ipv6 public address(es)
         "fe80::1",                                   #8 ipv6 link local address
         [1,],                                        #9 vlan id(s)
         ["192.168.1.1",],                            #10 parent(s) ip address
          2,                                          #11 monitorlist node position
          "182x186",                                  #12 LANmap position
          False,                                      #13 wireless connected to parent
          0,                                          #14 Canvas ID
          ""],                                        #15 icon (location)

          ["Home Server",                             #0 name
          "Servers",                                  #1 group
          "Server",                                   #2 type of device
          "Somewhere else",                           #3 location name
          True,                                       #4 reachable/pingable device
          "Online",                                   #5 node status
         ["192.168.1.3",],                            #6 ipv4 address(es)
         ["2001:0000:0000:0000:0000:0000:0000:0004",],#7 ipv6 public address(es)
         "fe80::1",                                   #8 ipv6 link local address
         [1,],                                        #9 vlan id(s)
         ["192.168.1.1",],                            #10 parent(s) ip address
          3,                                          #11 monitorlist node position
          "344x187",                                  #12 LANmap position
          False,                                      #13 wireless connected to parent
          0,                                          #14 Canvas ID
          ""],                                        #15 icon (location)

          ["Computer",                                #0 name
          "Computers",                                #1 group
          "Client",                                   #2 type of device
          "Livingroom",                               #3 location name
          True,                                       #4 reachable/pingable device
          "Offline",                                  #5 node status
         ["192.168.1.4",],                            #6 ipv4 address(es)
         ["2001:0000:0000:0000:0000:0000:0000:0005",],#7 ipv6 public address(es)
         "fe80::1",                                   #8 ipv6 link local address
         [1,],                                        #9 vlan id(s)
         ["Dumbswitch",],                             #10 parent(s) ip address
          4,                                          #11 monitorlist node position
          "182x298",                                  #12 LANmap position
          False,                                      #13 wireless connected to parent
          0,                                          #14 Canvas ID
          ""],                                        #15 icon (location)
        ]
nodes = nodesDefault

# Mapper settings

mapperImage = ""
mapperImageScaling = True
mapperNodeSize = 16 # size in pixels
mapperNodeStatusColorOnline = "00FF15"  #green
mapperNodeStatusColorOffline = "FF0000" #red
mapperNodeStatusColorAwaiting = "FF8400"#orange
mapperNodeStatusColorNoStatus = "00FFFF"#blue
mapperDrawLines = True #draws the lines between nodes
mapperShowLabels = True

# GUI settings
guiWindowSize = "1127x659"

# Logging settings
logEnabled = True
log = []
logInTerminal = False

def save():
	"""Save the current settings to settings.ini"""

	# lets try to write the config file
	try:
		f = open("settings.ini","w")
		f.write("\n")
		f.write("\n")
		f.write("#########################\n")
		f.write("# Configfile for LanMap #\n")
		f.write("#     Made by hcbd      #\n")
		f.write("#########################\n")
		f.write("\n")

		#Gui settings
		f.write("[Main Window]\n")
		f.write("WindowSize=" + guiWindowSize + "\n")
		f.write("\n")

		#Map settings
		f.write("[Map]\n")
		f.write("MapUpdateInterval=" + str(monitorUpdateInterval) + "\n")
		f.write("BgImageLocation=" + str(mapperImage) + "\n")
		f.write("BgImageScaling=" + str(mapperImageScaling) + "\n")
		f.write("NodeSize=" + str(mapperNodeSize) + "\n")
		f.write("DrawLinesBetweenNodes=" + str(mapperDrawLines) + "\n")
		f.write("NodeStatusColorOnline=" + str(mapperNodeStatusColorOnline) + "\n")
		f.write("NodeStatusColorOffline=" + str(mapperNodeStatusColorOffline) + "\n")
		f.write("NodeStatusColorAwaiting=" + str(mapperNodeStatusColorAwaiting) + "\n")
		f.write("NodeStatusColorNoStatus=" + str(mapperNodeStatusColorNoStatus) + "\n")
		f.write("\n")

		# save current nodes
		f.write("# Do not edit below !\n")
		f.write("\n")
		f.write("[Nodes]\n")
		nodecount = 0
		for node in nodes:
			f.write("" + str(nodecount) + ".name = " + str(node[0]) + "\n")
			f.write("" + str(nodecount) + ".group = " + str(node[1]) + "\n")
			f.write("" + str(nodecount) + ".type = " + str(node[2]) + "\n")
			f.write("" + str(nodecount) + ".location = " + str(node[3]) + "\n")
			f.write("" + str(nodecount) + ".pingable = " + str(node[4]) + "\n")
			f.write("" + str(nodecount) + ".status = Awaiting\n") # + str(node[5]) + for saving the status
			for ipv4 in node[6]:
				f.write("" + str(nodecount) + ".ipv4 = " + str(ipv4) + "\n")
			for ipv6 in node[7]:
				f.write("" + str(nodecount) + ".ipv6global = " + str(ipv6) + "\n")
			f.write("" + str(nodecount) + ".ipv6linklocal = " + str(node[8]) + "\n")
			for vlan in node[9]:
				f.write("" + str(nodecount) + ".vlan = " + str(vlan) + "\n")
			for parent in node[10]:
				f.write("" + str(nodecount) + ".parent = " + str(parent) + "\n")
			f.write("" + str(nodecount) + ".listposition = " + str(node[11]) + "\n")
			f.write("" + str(nodecount) + ".mapposition = " + str(node[12]) + "\n")
			f.write("" + str(nodecount) + ".wirelessToParent = " + str(node[13]) + "\n")
			#f.write("" + str(nodecount) + ".canvasId = " + str(node[14]) + "\n")
			#f.write("" + str(nodecount) + ".customIcon = " + str(node[15]) + "\n")
			f.write("\n")
			nodecount = nodecount + 1

		f.write("\n")
		f.write("\n")
		f.write("\n")
		f.close()
	except:
		print("error while writing to settings.ini file")

class MultiOrderedDict(OrderedDict):
    def __setitem__(self, key, value):
        if isinstance(value, list) and key in self:
            self[key].extend(value)
        else:
            super(OrderedDict, self).__setitem__(key, value)

def load():
	"""Load the settings from settings.ini"""
	# get nodes
	global nodes
	try:
		cfg = RawConfigParser(dict_type=MultiOrderedDict)
		cfg.read("settings.ini")

		# for some reason mulitordereddict gives an empty list with .options()
		cfgs = SafeConfigParser()
		cfgs.read("settings.ini")
		x = 0

		nodes = []

		for option in cfgs.options("Nodes"):
			# check each node for number
			parts = option.split(".")
			try:
				partsnr = int(parts[0])
			except:
				partsnr = "not an integer"
			if isinstance(partsnr, int) and partsnr >= 0:

				if partsnr == x:
					nodes.append(["","","","",True,"",["",],["",],"",[1,],["",],0,"",False,0,""])
					x = x + 1

				value = cfg.get("Nodes", option)

				if parts[1] == "name":
					nodes[partsnr][0] = (str(value[0]))

				if parts[1] == "group":
					nodes[partsnr][1] = str(value[0])

				if parts[1] == "type":
					nodes[partsnr][2] = str(value[0])

				if parts[1] == "location":
					nodes[partsnr][3] = str(value[0])

				if parts[1] == "pingable":
					if str(value[0])=="True":
						nodes[partsnr][4] = True
					if str(value[0])=="False":
						nodes[partsnr][4] = False

				if parts[1] == "status":
					nodes[partsnr][5] = str(value[0])

				if parts[1] == "ipv4":
					nodes[partsnr][6] = value

				if parts[1] == "ipv6global":
					nodes[partsnr][7] = value

				if parts[1] == "ipv6linklocal":
					nodes[partsnr][8] = str(value[0])

				if parts[1] == "vlan":
					nodes[partsnr][9] = []
					for var in value:
						nodes[partsnr][9].append(int(var))

				if parts[1] == "parent":
					nodes[partsnr][10] = value

				if parts[1] == "listposition":
					nodes[partsnr][11] = int(str(value[0]))

				if parts[1] == "mapposition":
					nodes[partsnr][12] = str(value[0])

				if parts[1] == "wirelesstoparent":
					if str(value[0])=="True" or str(value[0])=="true":
						nodes[partsnr][13] = True
					if str(value[0])=="False" or str(value[0])=="false":
						nodes[partsnr][13] = False

				#if parts[1] == "customIcon":
					#nodes[partsnr][14] = int(str(value[0]))

				#if parts[1] == "customIcon":
					#nodes[partsnr][15] = str(value[0])

		# get the rest of the vars
		global mapperImage, mapperImageScaling, mapperNodeSize
		global mapperNodeStatusColorOnline, mapperNodeStatusColorOffline
		global mapperNodeStatusColorAwaiting, mapperNodeStatusColorNoStatus
		global monitorUpdateInterval

		monitorUpdateInterval = str(cfgs.get("Map", "MapupdateInterval"))
		mapperImage = str(cfgs.get("Map", "BgImageLocation"))
		mapperImageScaling = str(cfgs.get("Map","BgImageScaling"))
		mapperNodeSize = int(cfgs.get("Map","NodeSize"))
		mapperNodeStatusColorOnline = str(cfgs.get("Map","NodeStatusColorOnline"))
		mapperNodeStatusColorOffline = str(cfgs.get("Map","NodeStatusColorOffline"))
		mapperNodeStatusColorAwaiting = str(cfgs.get("Map","NodeStatusColorAwaiting"))
		mapperNodeStatusColorNoStatus = str(cfgs.get("Map","NodeStatusColorNoStatus"))
		logger.add("Loaded last used config from settings.ini")
	except:
		# error with loading config file. Using default settings
		nodes = nodesDefault
		logger.add("Error importing settings.ini file, using default config")
