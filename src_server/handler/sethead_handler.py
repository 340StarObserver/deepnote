#!/usr/bin/python
# -*- coding:utf-8 -*-

# Author 		: 	Lv Yang
# Created 		: 	05 October 2016
# Modified 		: 	11 October 2016
# Version 		: 	1.0

"""
This script used to set a user's head image
"""

import base64
import random
import sys
sys.path.append("../model")

from base_handler import BaseHandler
from account_model import upload_head

class SetheadHandler(BaseHandler) :

    def __init__(self,post_data,post_files,usr_session,server_conf):
        super(SetheadHandler,self).__init__(post_data,post_files,usr_session,server_conf)

    def perform(self):
        # if not login
        if 'user_id' not in self._usr_session:
            return {'result':False,'reason':1}

        # if token is wrong
        token = int(self._post_data['token'])
        if 'token' not in self._usr_session or token != self._usr_session['token']:
            return {'result':False,'reason':2}

        # if failed to get head data
        head = None
        w = True
        try:
            head = base64.b64decode(self._post_data['head'])
        except Exception,e:
            w = False
            print str(e)
        if w is False:
            return {'result':False,'reason':3}

        # if failed to save head
        try:
            upload_head(self._server_conf['oss']['access_id'],self._server_conf['oss']['access_key'],\
                self._server_conf['oss']['end_point'],\
                self._server_conf['oss']['bucket'],\
                self._server_conf['oss']['head_dir'],\
                self._usr_session['user_id'],head)
        except Exception,e:
            w = False
            print str(e)
        if w is False:
            return {'result':False,'reason':4}

        # update head success, it should produce a new token
        token = random.randint(self._server_conf['auth']['token_min'],\
            self._server_conf['auth']['token_max'])
        self._usr_session['token'] = token

        # return result
        return {'result':True}
