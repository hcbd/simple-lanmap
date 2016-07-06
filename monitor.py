# -*- coding: utf-8 -*-

import settings as settings
import network as net
import log as log
import time
import thread

def start():
	"""Start monitoring of the given nodes in a thread"""
	settings.monitorRunning = True
	thread.start_new_thread(monitor,())
	#monitor()
	log.add("Monitoring Started")
	
def stop():
	"""Stop or interrupt monitor"""
	settings.monitorRunning = False
	log.add("Monitoring Stopped")
	
def monitor():
	"""ping each node and check if online"""
	
	status = False
	
	while settings.monitorRunning:
		for node in settings.nodes:
			nodeIPs = node[6]
			for ip in nodeIPs:
				if node[4]:
					status = net.ping(ip)
					if status == True:
						node[5] = "Online"
					if status == False:
						node[5] = "Offline"
						break # if any ip of node is offline, set node status to Offline
				else:
					node[5] = "NoStatus"
		
		time.sleep(settings.monitorPingInterval) # time between scans
