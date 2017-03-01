#!/usr/bin/python
# -*- coding:utf-8 -*-

# Author 		: 	Lv Yang
# Created 		: 	07 October 2016
# Modified 		: 	07 October 2016
# Version 		: 	1.0

"""
This file used to create a elasticsearch client
"""

from elasticsearch import Elasticsearch

def getclient(hosts):
    """
    create a elasticsearch client
    para hosts is like ["ip1:port1","ip2:port2","ip3:port3"]
    """
    conn = Elasticsearch(hosts,\
        sniff_on_start=True,\
        sniff_on_connection_fail=True,\
        sniffer_timeout=60)
    return conn
