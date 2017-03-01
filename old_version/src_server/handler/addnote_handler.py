#!/usr/bin/python
# -*- coding:utf-8 -*-

# Author 		: 	Lv Yang
# Created 		: 	05 October 2016
# Modified 		: 	12 October 2016
# Version 		: 	1.0

"""
This script used to add a new note
"""

import time
import random
import sys
sys.path.append("../model")

from base_handler import BaseHandler
from valid_model import is_valid_notetitle
from valid_model import is_valid_notefeel
import mongoconn_model
import esconn_model
from note_model import add_note_to_mongo
from note_model import add_note_to_es

class AddnoteHandler(BaseHandler) :

    def __init__(self,post_data,post_files,usr_session,server_conf):
        super(AddnoteHandler,self).__init__(post_data,post_files,usr_session,server_conf)

    def perform(self):
        # accept parameters
        token = int(self._post_data['token'])
        title = self._post_data['title']
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

        # if note's title is invalid
        if is_valid_notetitle(title) is False:
            return {'result':False,'reason':3}

        # if note's feel is invalid
        if is_valid_notefeel(feel) is False:
            return {'result':False,'reason':4}

        # insert this note to mongo
        db_conn = mongoconn_model.getclient(self._server_conf['mongo']['hosts'],\
            self._server_conf['mongo']['replset'],self._server_conf['mongo']['db_name'],\
            self._server_conf['mongo']['db_user'],self._server_conf['mongo']['db_pwd'])
        note_id = add_note_to_mongo(db_conn,self._server_conf['mongo']['db_name'],\
            title,self._usr_session['user_id'],self._usr_session['nick'],\
            feel,labels,source_link,source_ref)
        db_conn.close()

        # insert this note to elasticsearch
        es_conn = esconn_model.getclient(self._server_conf['elasticsearch']['hosts'])
        add_note_to_es(es_conn,\
            self._server_conf['elasticsearch']['index'],\
            self._server_conf['elasticsearch']['type'],\
            note_id,title,feel,labels,source_ref)

        # produce a new token and save it to session
        token = random.randint(self._server_conf['auth']['token_min'],\
            self._server_conf['auth']['token_max'])
        self._usr_session['token'] = token

        # return result
        return {'result':True,'token':token,'note_id':note_id,'pub_time':int(time.time())}
