#!/usr/bin/python
# -*- coding:utf-8 -*-

# Author 		: 	Lv Yang
# Created 		: 	05 October 2016
# Modified 		: 	22 October 2016
# Version 		: 	1.0

"""
This script used to care somebody or cancel care
"""

import time
import sys
sys.path.append("../model")

from base_handler import BaseHandler
from mongoconn_model import getclient
from interact_model import exist_care

class CareHandler(BaseHandler) :

    def __init__(self,post_data,post_files,usr_session,server_conf):
        super(CareHandler,self).__init__(post_data,post_files,usr_session,server_conf)

    def perform(self):
        # accept parameters
        cared_id = self._post_data['cared_id']

        # if not login
        if 'user_id' not in self._usr_session:
            return {'result':False,'reason':1}

        # connect to mongo
        db_conn = getclient(self._server_conf['mongo']['hosts'],\
            self._server_conf['mongo']['replset'],self._server_conf['mongo']['db_name'],\
            self._server_conf['mongo']['db_user'],self._server_conf['mongo']['db_pwd'])

        record_id = exist_care(db_conn,self._server_conf['mongo']['db_name'],\
            self._usr_session['user_id'],cared_id)
        if record_id is None:
            # if ever has not cared this person
            cur_t = int(time.time())
            # add a care record
            care_doc = {}
            care_doc['carer_id'] = self._usr_session['user_id']
            care_doc['time'] = cur_t
            care_doc['cared_id'] = cared_id
            db_conn[self._server_conf['mongo']['db_name']]['care_record'].insert_one(care_doc)
            # add a message to remind the cared person
            msg_doc = {}
            msg_doc['user_ids'] = [cared_id]
            msg_doc['time'] = cur_t
            msg_doc['who_id'] = self._usr_session['user_id']
            msg_doc['who_nick'] = self._usr_session['nick']
            msg_doc['note_id'] = ''
            msg_doc['note_title'] = ''
            msg_doc['action_id'] = 4
            msg_doc['content'] = ''
            db_conn[self._server_conf['mongo']['db_name']]['message_record'].insert_one(msg_doc)
        else:
            # if ever has cared this person
            db_conn[self._server_conf['mongo']['db_name']]['care_record'].delete_one({'_id':record_id})

        # return result
        db_conn.close()
        return {'result':True}
