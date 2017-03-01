#!/usr/bin/python
# -*- coding:utf-8 -*-

# Author 		: 	Lv Yang
# Created 		: 	07 October 2016
# Modified 		: 	07 October 2016
# Version 		: 	1.0

"""
This script used to initialize collections in mongodb
"""

import sys
sys.path.append("../model")

import conf_model
import mongoconn_model

def init_mongo(mongoconn,db_name):
    # 1. init collection 'user_info'
    mongoconn[db_name]['user_info'].drop()
    doc = {'_id':'13915497202'}
    mongoconn[db_name]['user_info'].insert_one(doc)
    mongoconn[db_name]['user_info'].remove({})
    print "init collection <user_info> success"

    # 2. init collection 'note_base'
    mongoconn[db_name]['note_base'].drop()
    doc = {'own_id':'13915497202','pub_time':1475599887}
    mongoconn[db_name]['note_base'].insert_one(doc)
    mongoconn[db_name]['note_base'].create_index([('own_id',1),('pub_time',-1)])
    mongoconn[db_name]['note_base'].create_index([('pub_time',-1)])
    mongoconn[db_name]['note_base'].remove({})
    print "init collection <note_base> success"

    # 3. init collection 'note_extra'
    mongoconn[db_name]['note_extra'].drop()
    doc = {}
    mongoconn[db_name]['note_extra'].insert_one(doc)
    mongoconn[db_name]['note_extra'].remove({})
    print "init collection <note_extra> success"

    # 4. init collection 'note_action'
    mongoconn[db_name]['note_action'].drop()
    doc = {'user_id':'13915497202','note_id':'123'}
    mongoconn[db_name]['note_action'].insert_one(doc)
    mongoconn[db_name]['note_action'].create_index([('user_id',1),('note_id',1)])
    mongoconn[db_name]['note_action'].remove({})
    print "init collection <note_action> success"

    # 5. init collection 'note_collect'
    mongoconn[db_name]['note_collect'].drop()
    doc = {'user_id':'13915497202','time':1475599887}
    mongoconn[db_name]['note_collect'].insert_one(doc)
    mongoconn[db_name]['note_collect'].create_index([('user_id',1),('time',-1)])
    mongoconn[db_name]['note_collect'].remove({})
    print "init collection <note_collect> success"

    # 6. init collection 'comment_record'
    mongoconn[db_name]['comment_record'].drop()
    doc = {'note_id':'123','ancestor_id':'0','time':1475599887}
    mongoconn[db_name]['comment_record'].insert_one(doc)
    mongoconn[db_name]['comment_record'].create_index([('note_id',1),('ancestor_id',1),('time',-1)])
    mongoconn[db_name]['comment_record'].remove({})
    print "init collection <comment_record> success"

    # 7. init collection 'message_record'
    mongoconn[db_name]['message_record'].drop()
    doc = {'user_ids':['13915497202','13915497203'],'time':1475599887}
    mongoconn[db_name]['message_record'].insert_one(doc)
    mongoconn[db_name]['message_record'].create_index([('user_ids',1),('time',-1)])
    mongoconn[db_name]['message_record'].remove({})
    print "init collection <message_record> success"

    # 8. init collection 'care_record'
    mongoconn[db_name]['care_record'].drop()
    doc = {'carer_id':'13915497202','time':1475599887}
    mongoconn[db_name]['care_record'].insert_one(doc)
    mongoconn[db_name]['care_record'].create_index([('carer_id',1),('time',-1)])
    mongoconn[db_name]['care_record'].remove({})
    print "init collection <care_record> success"


def entrance(confpath):
    # 1. read configuration
    conf = conf_model.read(confpath)
    # 2. create a mongo client
    conn = mongoconn_model.getclient(conf['mongo']['hosts'],conf['mongo']['replset'],\
        conf['mongo']['db_name'],conf['mongo']['db_user'],conf['mongo']['db_pwd'])
    # 3. do init
    init_mongo(conn,conf['mongo']['db_name'])
    # 4. close connection
    conn.close()
    # 5. all done
    print "all done"


if __name__ == '__main__':
    entrance("../conf/server.conf")
