# -*- coding: utf-8 -*-

import os, socket, sys
from array import *
from subprocess import Popen, STDOUT, DEVNULL

if os.name != "nt":
	import fcntl
	import struct

def validIp4(address):
	"""check if the given Ip address is a IPv4 address"""
	check = False								# simplecheck if IP address
	chars = set("012345.")
	parts = address.split(".")

	if len(parts) == 4 and parts[0] != "" and parts[1] != "" and parts[2] != "" and parts[3] != "":
		if len(address) > 6 or len(address) < 16:
			if (len(parts[0]) > 0 and len(parts[0]) < 4) and (len(parts[1]) > 0 and len(parts[1]) < 4) and (len(parts[2]) > 0 and len(parts[2]) < 4) and (len(parts[3]) > 0 and len(parts[3]) < 4):
				if any((c in chars) for c in address):
					check = True
	return check

def validIp6(address):
	"""check if given ip address is an valid IPv6 address"""
	#nothing here yet.
	return True

def getMyIp():
	"""get the current ip address of the computer and return a string"""
	ip = socket.gethostbyname(socket.gethostname()) 	#windows/Linux easy way

	if ip.startswith("127.") and os.name != "nt": 		#linux hard way if hostsfile ain't cooperating
		interfaces = [b"eth0",b"eth1",b"eth2",b"wlan0",b"wlan1",b"wifi0",b"ath0",b"ath1",b"ppp0"]
		for ifname in interfaces:
			try:
				s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
				ip = socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', ifname[:15]))[20:24])
			except IOError:
				pass
	return ip

def ping_windows(address, timeout=1, count=1):
	"""Ping address and return True if the host responded in time."""
	# Windows' ping takes a timeout value in milliseconds.
	args = ('ping', address, '-n', str(count), '-w', str(timeout*1000))
	with Popen(args, stdout=DEVNULL, stderr=STDOUT) as proc:
		return proc.wait() == 0

def ping_linux(address, timeout=1, count=1):
	"""Ping address and return True if the host responded in time."""
	args = ('ping', address, '-c', str(count), '-W', str(timeout))
	with Popen(args, stdout=DEVNULL, stderr=STDOUT) as proc:
		return proc.wait() == 0

# Choose the ping function depending on platform.
ping = ping_windows if sys.platform == 'win32' else ping_linux

def dhcpDetect():
	"""listen for (rouge) dhcp servers
	   returns a list with found/broadcasting dhcp servers"""
	# This must happen without running as root
	pass
