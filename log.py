# -*- coding: utf-8 -*-
import time
import settings as settings

def add(msg):
	"""add current time, message and status to the log"""
	
	currentTime = time.strftime("%d-%m-%Y %H:%M:%S")
	msg = currentTime + " -> " + msg
	settings.log.append(str(msg))
	
def clear():
	"""clear the log"""
	settings.log = []

def save():
	"""save the log to a file"""
	pass
