#!/usr/bin/python
# -*- coding:utf-8 -*-

# Author 		: 	Lv Yang
# Created 		: 	05 October 2016
# Modified 		: 	05 October 2016
# Version 		: 	1.0

"""
This file used to create a mongo client
"""

from pymongo import MongoClient
from pymongo import ReadPreference

def getclient(hosts,replicaset,db_name,db_user,db_pwd):
    """
    create a mongo client
    parameters :
        hosts is the ip:ports of a replicaset, like 'host1:port1,host2:port2,host3:port3'
        replicaset is the name of your replicaset
        db_name is the name of your database
        db_user,db_pwd is for auth
    """
    conn = MongoClient(hosts,replicaSet=replicaset,read_preference=ReadPreference.SECONDARY_PREFERRED)
    conn[db_name].authenticate(db_user,db_pwd,mechanism='SCRAM-SHA-1')
    return conn
