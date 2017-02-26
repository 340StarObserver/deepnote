#!/usr/bin/python
# -*- coding:utf-8 -*-

# Author 		: 	Lv Yang
# Created 		: 	24 September 2016
# Modified 		: 	24 September 2016
# Version 		: 	1.0

"""
This script used to read configuration from a file
"""

import ConfigParser
import sys

def read(filename):
    """
    this function used to read configuration from a file

    the parameter is the path of file
    it returns a dictionary of pairs of <key,value>
    """
    res = {'oss':{},'mongo':{},'appserver':{}}
    config = ConfigParser.ConfigParser()
    try:
        config.read(filename)
        # about oss
        res['oss']['access_id'] = config.get('oss','access_id')
        res['oss']['access_key'] = config.get('oss','access_key')
        res['oss']['end_point'] = config.get('oss','end_point')
        res['oss']['bucket'] = config.get('oss','bucket')
        res['oss']['head_dir'] = config.get('oss','head_dir')
        # about mongo
        res['mongo']['hosts'] = config.get('mongo','hosts')
        res['mongo']['replset'] = config.get('mongo','replset')
        res['mongo']['db_name'] = config.get('mongo','db_name')
        res['mongo']['db_user'] = config.get('mongo','db_user')
        res['mongo']['db_pwd'] = config.get('mongo','db_pwd')
        # about webserver
        res['appserver']['rsa_length'] = int(config.get('appserver','rsa_length'))
    except Exception,e:
        print "fail to read configuration from %s"%(filename)
        print str(e)
        sys.exit(1)
    return res


if __name__ == '__main__':
    conf = read("../conf/server.conf")
    print conf
