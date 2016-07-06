# -*- coding: utf-8 -*-

import settings as settings
import network as network
import log as log


def start():
	"""start a scan in a thread"""
	settings.scanRunning = True
	log.add("Started scanning")
	# start a scan in a thread
	pass

def stop():
	"""interupt the currently running scan"""
	settings.scanRunning = False
	pass

def buildScanList(startIp,endIp):
	"""build from the input a list of hosts to scan"""

	# Checking if I got valid Ip's
	if network.validIp4(startIp) and network.validIp4(endIp):
		startIpseg = startIp.split(".")
		endIpseg = endIp.split(".")
		if startIpseg[0] < endIpseg[0]:
			#print("range to big")
			return False
	else:
		#print("wrong ip")
		return False

	# ip segments to integers
	startIpseg1 = int(startIpseg[0])
	startIpseg2 = int(startIpseg[1])
	startIpseg3 = int(startIpseg[2])
	startIpseg4 = int(startIpseg[3])
	endIpseg1 = int(endIpseg[0])
	endIpseg2 = int(endIpseg[1])
	endIpseg3 = int(endIpseg[2])
	endIpseg4 = int(endIpseg[3])

	# quick check if logical start/stop addresses
	if startIpseg2 > endIpseg2 and startIpseg1 >= endIpseg1:
		#print("startip / stopip is wrong 1")
		return False
	if startIpseg3 > endIpseg3 and startIpseg2 >= endIpseg2:
		#print("startip / stopip is wrong 2 ")
		return False
	if startIpseg4 > endIpseg4 and startIpseg3 >= endIpseg3 and startIpseg2 == endIpseg2:
		#print("startip / stopip is wrong 3")
		return False

	# Nodes to scan / scanlist

	scanNodes = []

	# Build Node-Scanlist - this isn't working correctly.
	for seg2 in range(startIpseg2, endIpseg2 +1):
		if seg2 == startIpseg2:
			for seg3 in range(startIpseg3, 256):
					for seg4 in range(startIpseg4, 255):
						print("1: ",startIpseg1, seg2, seg3, seg4)
						scanNodes.append(str(startIpseg1) + "." + str(seg2) + "." + str(seg3) + "." + str(seg4))
		if seg2 < endIpseg2 and seg2 > startIpseg2:
			for seg3 in range(1, 256):
				for seg4 in range(1, 255):
					print("2: ",startIpseg1, seg2, seg3, seg4)
					scanNodes.append(str(startIpseg1) + "." + str(seg2) + "." + str(seg3) + "." + str(seg4))
		if seg2 == endIpseg2:
			for seg3 in range(1, endIpseg3 + 1):
				if seg3 == startIpseg3:
					for seg4 in range(startIpseg4, 255):
						print("3: ",startIpseg1, seg2, seg3, seg4)
						scanNodes.append(str(startIpseg1) + "." + str(seg2) + "." + str(seg3) + "." + str(seg4))
				if seg3 < endIpseg3 and seg3 > startIpseg3:
					for seg4 in range(1,255):
						print("4: ",startIpseg1, seg2, seg3, seg4)
						scanNodes.append(str(startIpseg1) + "." + str(seg2) + "." + str(seg3) + "." + str(seg4))
				if seg3 == endIpseg3:
					print("5: ",startIpseg1, seg2, seg3, seg4)
					for seg4 in range(1, endIpseg4 + 1):
						scanNodes.append(str(startIpseg1) + "." + str(seg2) + "." + str(seg3) + "." + str(seg4))

	#print("\nresulting list:")
	#print(scanNodes)

	if not scanNodes == []:
		return True
		settings.scanNodes = scanNodes
	else:
		return False
		#print("no nodes")

def scanInTread():
	"""ping each address in the given range and set nodes status. Return errors"""

