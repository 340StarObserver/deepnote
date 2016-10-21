#!/usr/bin/python
# -*- coding:utf-8 -*-

# Author 		: 	Lv Yang
# Created 		: 	05 October 2016
# Modified 		: 	21 October 2016
# Version 		: 	1.0

"""
This script used to oppose a note or cancel oppose
"""

import time
import sys
sys.path.append("../model")

from base_handler import BaseHandler
from mongoconn_model import getclient
from note_model import exist_note
from interact_model import affect_note
from interact_model import agree_oppose_record
from interact_model import agree_oppose_add
from interact_model import agree_oppose_delete

class OpposeHandler(BaseHandler) :

    def __init__(self,post_data,post_files,usr_session,server_conf):
        super(OpposeHandler,self).__init__(post_data,post_files,usr_session,server_conf)

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
            # get ever agree or oppose record
            ever_action = agree_oppose_record(db_conn,\
                self._server_conf['mongo']['db_name'],\
                self._usr_session['user_id'],note_id)
            if ever_action is None:
                # if ever havn't agreed or opposed
                response['result'] = True
                # increase this note's oppose_num
                affect_note(db_conn,self._server_conf['mongo']['db_name'],note_id,'oppose_num',1)
                # add record that this user oppose this note
                agree_oppose_add(db_conn,self._server_conf['mongo']['db_name'],\
                    self._usr_session['user_id'],note_id,1)
                # add a message to remind this note's owner
                doc = {}
                doc['user_ids'] = [own_id]
                doc['time'] = int(time.time())
                doc['who_id'] = self._usr_session['user_id']
                doc['who_nick'] = self._usr_session['nick']
                doc['note_id'] = note_id
                doc['note_title'] = note_title
                doc['action_id'] = 2
                doc['content'] = ''
                db_conn[self._server_conf['mongo']['db_name']]['message_record'].insert_one(doc)
            elif ever_action is 1:
                # if ever has opposed this note
                response['result'] = True
                # decrease this note's oppose_num
                affect_note(db_conn,self._server_conf['mongo']['db_name'],note_id,'oppose_num',-1)
                # delete the ever oppose record
                agree_oppose_delete(db_conn,self._server_conf['mongo']['db_name'],\
                    self._usr_session['user_id'],note_id,1)
            else:
                # if ever has agreed this note
                response['reason'] = 3

        # return result
        db_conn.close()
        return response
