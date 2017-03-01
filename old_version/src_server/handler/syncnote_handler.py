#!/usr/bin/python
# -*- coding:utf-8 -*-

# Author 		: 	Lv Yang
# Created 		: 	05 October 2016
# Modified 		: 	12 October 2016
# Version 		: 	1.0

"""
This script used to sync a user's all notes
"""

import random
import sys
sys.path.append("../model")

from base_handler import BaseHandler
from mongoconn_model import getclient

class SyncnoteHandler(BaseHandler) :

    def __init__(self,post_data,post_files,usr_session,server_conf):
        super(SyncnoteHandler,self).__init__(post_data,post_files,usr_session,server_conf)

    def perform(self):
        # if not login
        if 'user_id' not in self._usr_session:
            return {'result':False,'reason':1}

        # if token is wrong
        if 'token' not in self._usr_session or int(self._post_data['token']) != self._usr_session['token']:
            return {'result':False,'reason':2}

        # connect to mongo
        db_conn = getclient(self._server_conf['mongo']['hosts'],\
            self._server_conf['mongo']['replset'],self._server_conf['mongo']['db_name'],\
            self._server_conf['mongo']['db_user'],self._server_conf['mongo']['db_pwd'])

        # produce a new token
        token = random.randint(self._server_conf['auth']['token_min'],\
            self._server_conf['auth']['token_max'])
        self._usr_session['token'] = token

        # do search
        response = {'result':True,'token':token,'notes':[]}
        notes = db_conn[self._server_conf['mongo']['db_name']]['note_base'].find(\
            {'own_id':self._usr_session['user_id']})
        factor_1 = {'_id':None}
        factor_2 = {'_id':0,'source_link':1,'source_ref':1}
        for note in notes:
            factor_1['_id'] = note['_id']
            extra_info = db_conn[self._server_conf['mongo']['db_name']]['note_extra'].find_one(\
                factor_1,factor_2)
            note['_id'] = str(note['_id'])
            if extra_info is not None:
                note['source_link'] = extra_info['source_link']
                note['source_ref'] = extra_info['source_ref']
            response['notes'].append(note)

        # return result
        db_conn.close()
        return response
