#!/usr/bin/python
# -*- coding:utf-8 -*-

# Author 		: 	Lv Yang
# Created 		: 	05 October 2016
# Modified 		: 	22 October 2016
# Version 		: 	1.0

"""
This script used to write a comment
"""

import time
import sys
sys.path.append("../model")

from base_handler import BaseHandler
from mongoconn_model import getclient
from note_model import exist_note
from interact_model import affect_note

class WritecommentHandler(BaseHandler) :

    def __init__(self,post_data,post_files,usr_session,server_conf):
        super(WritecommentHandler,self).__init__(post_data,post_files,usr_session,server_conf)

    def perform(self):
        # accept parameters
        note_id = self._post_data['note_id']
        note_title = self._post_data['note_title']
        ancestor_id = self._post_data['ancestor_id']
        content = self._post_data['content']
        replyed_nick = self._post_data['replyed_nick']
        recv_ids = self._post_data['recv_ids']
        if len(recv_ids) == 0:
            recv_ids = []
        else:
            recv_ids = recv_ids.split(',')

        # if not login
        if 'user_id' not in self._usr_session:
            return {'result':False,'reason':1}

        # if the content is empty
        if len(content) == 0:
            return {'result':False,'reason':3}

        # connect to mongo
        db_conn = getclient(self._server_conf['mongo']['hosts'],\
            self._server_conf['mongo']['replset'],self._server_conf['mongo']['db_name'],\
            self._server_conf['mongo']['db_user'],self._server_conf['mongo']['db_pwd'])

        response = {'result':False}
        if exist_note(db_conn,self._server_conf['mongo']['db_name'],note_id) is None:
            # if this note not exist
            response['reason'] = 2
        else:
            cur_t = int(time.time())
            response['result'] = True
            # increase this note's comment_num
            affect_note(db_conn,self._server_conf['mongo']['db_name'],note_id,'comment_num',1)
            # add a message to remind all the associated people
            msg_doc = {}
            msg_doc['user_ids'] = recv_ids
            msg_doc['time'] = cur_t
            msg_doc['who_id'] = self._usr_session['user_id']
            msg_doc['who_nick'] = self._usr_session['nick']
            msg_doc['note_id'] = note_id
            msg_doc['note_title'] = note_title
            msg_doc['action_id'] = 0
            msg_doc['content'] = content
            db_conn[self._server_conf['mongo']['db_name']]['message_record'].insert_one(msg_doc)
            # add a comment of this note
            comment_doc = {}
            comment_doc['note_id'] = note_id
            comment_doc['ancestor_id'] = ancestor_id
            comment_doc['time'] = cur_t
            comment_doc['content'] = content
            comment_doc['send_id'] = self._usr_session['user_id']
            comment_doc['send_nick'] = self._usr_session['nick']
            comment_doc['replyed_nick'] = replyed_nick
            recv_ids.append(self._usr_session['user_id'])
            comment_doc['recv_ids'] = recv_ids
            db_conn[self._server_conf['mongo']['db_name']]['comment_record'].insert_one(comment_doc)

        # return result
        db_conn.close()
        return response
