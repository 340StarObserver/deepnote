#!/usr/bin/python
# -*- coding:utf-8 -*-

# Author 		: 	Lv Yang
# Created 		: 	05 October 2016
# Modified 		: 	21 October 2016
# Version 		: 	1.0

"""
This script used to collect a note or cancel collect
"""

import time
import sys
sys.path.append("../model")

from base_handler import BaseHandler
from mongoconn_model import getclient
from note_model import exist_note
from interact_model import affect_note
from interact_model import exist_collect

class CollectHandler(BaseHandler) :

    def __init__(self,post_data,post_files,usr_session,server_conf):
        super(CollectHandler,self).__init__(post_data,post_files,usr_session,server_conf)

    def perform(self):
        # accept parameters
        note_id = self._post_data['note_id']
        note_title = self._post_data['note_title']
        own_id = self._post_data['own_id']

        # if not login
        if 'user_id' not in self._usr_session:
            return {'result':False,'reason':1}

        # connect to mongo
        db_conn = getclient(self._server_conf['mongo']['hosts'],\
            self._server_conf['mongo']['replset'],self._server_conf['mongo']['db_name'],\
            self._server_conf['mongo']['db_user'],self._server_conf['mongo']['db_pwd'])

        response = {'result':False}
        if exist_note(db_conn,self._server_conf['mongo']['db_name'],note_id) is None:
            # if that note not exist
            response['reason'] = 2
        else:
            response['result'] = True
            collect_id = exist_collect(db_conn,self._server_conf['mongo']['db_name'],\
                self._usr_session['user_id'],note_id)
            if collect_id is None:
                # if ever has not collected this note
                # increase this note's collect_num
                affect_note(db_conn,self._server_conf['mongo']['db_name'],note_id,'collect_num',1)
                # add a collect record
                collect_doc = {}
                cur_t = int(time.time())
                collect_doc['user_id'] = self._usr_session['user_id']
                collect_doc['time'] = cur_t
                collect_doc['note_id'] = note_id
                db_conn[self._server_conf['mongo']['db_name']]['note_collect'].insert_one(collect_doc)
                # add a message to remind this note's owner
                msg_doc = {}
                msg_doc['user_ids'] = [own_id]
                msg_doc['time'] = cur_t
                msg_doc['who_id'] = self._usr_session['user_id']
                msg_doc['who_nick'] = self._usr_session['nick']
                msg_doc['note_id'] = note_id
                msg_doc['note_title'] = note_title
                msg_doc['action_id'] = 3
                msg_doc['content'] = ''
                db_conn[self._server_conf['mongo']['db_name']]['message_record'].insert_one(msg_doc)
            else:
                # if ever has collected this note
                # decrease this note's collect_num
                affect_note(db_conn,self._server_conf['mongo']['db_name'],note_id,'collect_num',-1)
                # delete the collect record
                db_conn[self._server_conf['mongo']['db_name']]['note_collect'].delete_one({'_id':collect_id})

        # return result
        db_conn.close()
        return response
