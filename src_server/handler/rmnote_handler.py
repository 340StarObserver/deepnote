#!/usr/bin/python
# -*- coding:utf-8 -*-

# Author 		: 	Lv Yang
# Created 		: 	05 October 2016
# Modified 		: 	12 October 2016
# Version 		: 	1.0

"""
This script used to remove a note
"""

import random
import sys
sys.path.append("../model")

from base_handler import BaseHandler
import mongoconn_model
import esconn_model
from note_model import exist_note
from note_model import delete_note_from_mongo
from note_model import delete_note_from_es

class RmnoteHandler(BaseHandler) :

    def __init__(self,post_data,post_files,usr_session,server_conf):
        super(RmnoteHandler,self).__init__(post_data,post_files,usr_session,server_conf)

    def perform(self):
        # accept parameters
        token = int(self._post_data['token'])
        note_id = self._post_data['note_id']

        # if not login
        if 'user_id' not in self._usr_session:
            return {'result':False,'reason':1}

        # if token is wrong
        if 'token' not in self._usr_session or token != self._usr_session['token']:
            return {'result':False,'reason':2}

        # connect to mongo
        db_conn = mongoconn_model.getclient(self._server_conf['mongo']['hosts'],\
            self._server_conf['mongo']['replset'],self._server_conf['mongo']['db_name'],\
            self._server_conf['mongo']['db_user'],self._server_conf['mongo']['db_pwd'])

        # connect to elasticsearch
        es_conn = esconn_model.getclient(self._server_conf['elasticsearch']['hosts'])

        response = {'result':True}
        note_owner = exist_note(db_conn,self._server_conf['mongo']['db_name'],note_id)
        if note_owner is None:
            # if this note not exist
            response['result'] = False
            response['reason'] = 3
        elif note_owner != self._usr_session['user_id']:
            # if this note exists and it isn't yours
            response['result'] = False
            response['reason'] = 4
        else:
            # if this note exists and it is yours
            # delete this note
            delete_note_from_mongo(db_conn,self._server_conf['mongo']['db_name'],note_id)
            delete_note_from_es(es_conn,\
                self._server_conf['elasticsearch']['index'],\
                self._server_conf['elasticsearch']['type'],\
                note_id)
            # produce a new token
            token = random.randint(self._server_conf['auth']['token_min'],\
                self._server_conf['auth']['token_max'])
            self._usr_session['token'] = token
            response['token'] = token

        # return result
        db_conn.close()
        return response
