# -*- coding: utf-8 -*-

# All network functions are located in this file under the 'net' class

import sys
import ipaddress
from subprocess import Popen, STDOUT, DEVNULL


def ping_windows(ipaddr, timeout, count):
    """Ping an IPv4 address on a Windows OS
       Return True if ipaddress is reachable on the network"""
    # windows ping takes the timeout value in milliseconds
    args = ('ping', ipaddr, '-n', str(count), '-w', str(timeout * 1000))
    with Popen(args, stdout=DEVNULL, stderr=STDOUT) as proc:
        return proc.wait() == 0


def ping6_windows(ipaddr, timeout, count, interface):
    """Ping an IPv6 address on a Windows OS
       Return True if ipaddress is reachable on the network"""
    # windows ping takes the timeout value in milliseconds
    args = ('ping6', ipaddr, '%', interface, '-n', str(count), '-w', str(timeout * 1000))
    with Popen(args, stdout=DEVNULL, stderr=STDOUT) as proc:
        return proc.wait() == 0


def ping_linux(ipaddr, timeout, count):
    """Ping an IPv4 address on a Linux OS
       Return True if ipaddress is reachable on the network"""
    args = ('ping', ipaddr, '-c', str(count), '-W', str(timeout))
    with Popen(args, stdout=DEVNULL, stderr=STDOUT) as proc:
        return proc.wait() == 0


def ping6_linux(ipaddr, timeout, count, interface):
    """Ping an IPv6 address on a Linux OS
       Return True if ipaddress is reachable on the network"""
    args = ('ping6', ipaddr, '%', interface, '-c', str(count), '-W', str(timeout))
    with Popen(args, stdout=DEVNULL, stderr=STDOUT) as proc:
        return proc.wait() == 0


def ping(ipaddr, timeout=1, count=1, interface=False):
    """Ping on depending on platform and ipv4 or ipv6 addresses and
       return True if ping gets a response"""
    if is_valid_ip4(ipaddr):
        if sys.platform == 'win32':
            result = ping_windows(ipaddr, timeout, count)
        else:
            result = ping_linux(ipaddr, timeout, count)
        return result
    elif is_valid_ip6(ipaddr):
        if not interface:
            return False
        if sys.platform == 'win32':
            result = ping6_windows(ipaddr, timeout, count)
        else:
            result = ping6_linux(ipaddr, timeout, count)
        return result
    else:
        return False


def get_hostname(ipaddr):
    """Returns the hostname of the device or False when none is present"""
    #TODO
    return False


def get_my_ip():
    """Returns the connected interface(s) and their ipaddress(es)"""
    #TODO
    return '0.0.0.0'


def get_interface():
    """returns the connected interface and filters out loopback adapters etc"""
    #TODO
    return 'eth0'


def is_valid_ip4(ipaddr):
    """Returns True if ipaddr is a valid IPv4 address"""
    try:
        test = ipaddress.IPv4Address(ipaddr)
        if test:
            return True
    except:
        return False


def is_valid_ip6(ipaddr):
    """Returns True if ipaddr is a valid IPv6 address"""
    try:
        test = ipaddress.IPv6Address(ipaddr)
        if test:
            return True
    except:
        return False