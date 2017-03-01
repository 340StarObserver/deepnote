#!/usr/bin/python
# -*- coding:utf-8 -*-

# Author 		: 	Lv Yang
# Created 		: 	07 October 2016
# Modified 		: 	07 October 2016
# Version 		: 	1.0

"""
This script used to initialize types in elasticsearch
"""

import sys
sys.path.append("../model")

from elasticsearch import client

import conf_model
import esconn_model

def produce_mappings(es_type):
    properties = {}
    properties['note_id'] = {"type":"string"}
    properties['title'] = {"type":"string","analyzer":"ik_smart"}
    properties['ref'] = {"type":"string","analyzer":"ik_max_word"}
    properties['feel'] = {"type":"string","analyzer":"ik_max_word"}
    properties['labels'] = {"type":"string","analyzer":"ik_max_word"}
    return {"mappings":{es_type:{"properties":properties}}}


def entrance(confpath):
    # 1. read configuration
    conf = conf_model.read(confpath)
    # 2. create a common elasticsearch client
    client_conn = esconn_model.getclient(conf['elasticsearch']['hosts'])
    index_conn = client.IndicesClient(client_conn)
    # 3. initialize properties
    try:
        index_conn.delete(index=conf['elasticsearch']['index'])
        print "delete the origin index success"
    except Exception,e:
        print str(e)
        print "delete the origin index failed"
    try:
        settings = produce_mappings(conf['elasticsearch']['type'])
        index_conn.create(index=conf['elasticsearch']['index'],body=settings)
        print "create index and init success"
    except Exception,e:
        print str(e)
        print "create index failed"


if __name__ == '__main__':
    entrance("../conf/server.conf")
