# -*- coding: utf-8 -*-

# Monitor the nodes for Availability
import time
import _thread

import settings
import log
import nodes
import network


def start():
    """Start monitoring the nodelist in a thread"""
    settings.monitor_running = True
    _thread.start_new_thread(monitor_nodes, ())
    log.add('Lanmonitor started')


def stop():
    """Stop monitoring of the nodelist"""
    settings.monitor_running = False
    log.add('Lanmonitor stopped')


def monitor_nodes():
    """Ping all nodes in the list at an given interval
       and change the node status to the fetched one"""
       #TODO: ipv6 support
    while settings.monitor_running:
        # load each node in list
        for node in nodes.nodelist:
            if node.check_status:
                # ping every given ipv4 per node
                for ip in node.ipv4:
                    if network.ping(ip):
                        node.status = "online"
                    else:
                        node.status = "offline"
            else:
                node.status = "nostatus"
        # monitor/ping nodes every x seconds
        time.sleep(settings.monitor_interval)