# -*- coding: utf-8 -*-
import time
import settings


log = []


def add(msg):
    """add an entry into the log with an optional timestamp"""
    if not settings.log_enabled:
        return 0
    if settings.log_timestamp_enabled:
        timestamp = time.strftime("%d-%m-%Y %H:%M:%S")
        msg = timestamp + ' - ' + msg
    log.append(msg)


def last():
    """returns the last entry in the log"""
    latest_entry = len(log)
    return log[latest_entry - 1]


def clear():
    """remove all entries from the log"""
    global log
    log = []


def save_to_disk(save_name):
    """save the log file to disk with the given location"""
    try:
        save_name = save_name + '.txt'
        f = open(save_name, "w")
        for line in log:
            f.write(line)
        return True
    except:
        add("Error saving log to file")
        return False