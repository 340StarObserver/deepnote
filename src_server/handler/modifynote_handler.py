#!/usr/bin/python
# -*- coding:utf-8 -*-

# Author 		: 	Lv Yang
# Created 		: 	05 October 2016
# Modified 		: 	12 October 2016
# Version 		: 	1.0

"""
This script used to modify a note
"""

import random
import sys
sys.path.append("../model")

from base_handler import BaseHandler
from valid_model import is_valid_notefeel
import mongoconn_model
import esconn_model
from note_model import exist_note
from note_model import modify_note_in_mongo
from note_model import modify_note_in_es

class ModifynoteHandler(BaseHandler) :

    def __init__(self,post_data,post_files,usr_session,server_conf):
        super(ModifynoteHandler,self).__init__(post_data,post_files,usr_session,server_conf)

    def perform(self):
        # accept parameters
        token = int(self._post_data['token'])
        note_id = self._post_data['note_id']
        labels = self._post_data['labels']
        source_link = self._post_data['source_link']
        source_ref = self._post_data['source_ref']
        feel = self._post_data['feel']

        # if not login
        if 'user_id' not in self._usr_session:
            return {'result':False,'reason':1}

        # if token is wrong
        if 'token' not in self._usr_session or token != self._usr_session['token']:
            return {'result':False,'reason':2}

        # if note's feel is invalid
        if is_valid_notefeel(feel) is False:
            return {'result':False,'reason':3}

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
            response['reason'] = 4
        elif note_owner != self._usr_session['user_id']:
            # if this note exists and it isn't yours
            response['result'] = False
            response['reason'] = 5
        else:
            # if this note exists and it is yours
            # update this note
            modify_note_in_mongo(db_conn,self._server_conf['mongo']['db_name'],\
                note_id,feel,labels,source_link,source_ref)
            modify_note_in_es(es_conn,self._server_conf['elasticsearch']['index'],\
                self._server_conf['elasticsearch']['type'],\
                note_id,feel,labels,source_ref)
            # produce a new token
            token = random.randint(self._server_conf['auth']['token_min'],\
                self._server_conf['auth']['token_max'])
            self._usr_session['token'] = token
            response['token'] = token

        # return result
        db_conn.close()
        return response
