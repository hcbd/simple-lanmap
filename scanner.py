# -*- coding: utf-8 -*-

# scan a network for devices with this module

import settings
import log
import network
import ipaddress
import _thread
from subprocess import Popen, STDOUT, PIPE


def start_ipv4_scan(begin_address, end_address):
    """Start a IPv4 scan in a thread"""
    _thread.start_new_thread(scan_ipv4, (begin_address, end_address))


def start_ipv6_scan(interface):
    """Start a IPv6 scan in a thread"""
    _thread.start_new_thread(scan_ipv6, ())


def stop():
    """Stop/cancel the current running scan"""
    settings.scanner_running = False


def scan_ipv4(begin_address, end_address):
    """Ping a range of IPv4 addresses return False if input is incorrect"""
    # need 2 lists for scanning and results
    scanlist = []
    foundlist = []

    # test if ip is valid
    start_ip = False
    stop_ip = False
    try:
        start_ip = ipaddress.IPv4Address(begin_address)
        stop_ip = ipaddress.IPv4Address(end_address)
        if start_ip > stop_ip:
            return False
    except:
        return False

    # build scanlist
    if start_ip and stop_ip:
        # convert ip's to integer for easy generating of list
        start_int = int(ipaddress.ip_address(start_ip))
        stop_int = int(ipaddress.ip_address(stop_ip))
        for ip_int in range(start_int, stop_int + 1):
            try:
                scanlist.append(str(ipaddress.ip_address(ip_int)))
            except:
                return False
    else:
        return False

    # ping each ip in the scanlist
    settings.scanner_running = True
        # needs a way to be faster: max 10 threads at the same
        # time to ease on system and network.
    for ip in scanlist:
        if settings.scanner_running:
            ping = network.ping(ip)
            if ping:
                foundlist.append(ip)
                settings.scanner_scan_result = foundlist
    settings.scanner_running = False

    if not foundlist == []:
        settings.scanner_scan_result = foundlist
        logmsg = "IPv4 scan completed: found "
        logmsg += str(len(foundlist)) + " devices in scanrange "
        logmsg += begin_address + "-" + end_address
        log.add(logmsg)
        return True
    else:
        logmsg = "IPv4 scan completed: nothing found in scanrange "
        logmsg += begin_address + "-" + end_address
        log.add(logmsg)
        return False


def scan_ipv6(interface):
    """scan for devices in the local IPv6 range, this done by a
       multicast ping on the local network, searching for
       fe80 addresses"""
    addr_int = 'ff02::1%' + interface
    args = ['ping6', addr_int, '-c', '10', '-W', '3']
    settings.scanner_running = True
    with Popen(args, stdout=PIPE, stderr=STDOUT) as proc:
        foundlist = []
        output = proc.communicate()
        lines = str(output[0])
        for line in lines.split("bytes from"):
            if line != '':
                line = str(line)
                start_index = line.find('fe80::')
                stop_index = line.find(interface) - 1
                if start_index == -1 or start_index == -2:
                    continue
                if stop_index == -1 or stop_index == -2:
                    continue
                address = line[start_index:stop_index]
                if network.is_valid_ip6(address):
                    if not address in foundlist:
                        foundlist.append(address)
            else:
                break
    settings.scanner_running = False
    # put results into global scanlist
    if not foundlist == []:
        settings.scanner_scan_result = foundlist
        log.add("IPv6 scan completed: found " + str(len(foundlist)) + " devices")
        return True
    else:
        log.add("IPv6 scan completed: nothing found")
        return False


class presets(object):
    """class for handling scan presets"""

    def __init__(self):
        self.list = []
        self.load()

    def new(self):
        """make a new preset with the following default entries"""
        self.name = 'New Preset'
        self.start_ip = '192.168.1.1'
        self.end_ip = '192.168.1.254'
        self.get_hostnames = False
        self.set_timeout = 2  # in seconds

    def add(self, name, start_ip, end_ip, get_hostnames, slow_network):
        tup = (name, start_ip, end_ip, get_hostnames, slow_network)
        self.list.append(tup)

    def save(self):
        """add the preset to the list and save to the preset file"""
        try:
            #TODO
            return True
        except:
            log.add("Error saving log file")
            return False

    def load(self):
        """load the presets from the presets file"""
        #TODO
        # testpreset
        self.add("Default Preset", "192.168.1.1", "192.168.1.254", False, 2)
        # end testpreset
        pass