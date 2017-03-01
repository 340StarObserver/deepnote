#!/usr/bin/python
# -*- coding:utf-8 -*-

# Author 		: 	Lv Yang
# Created 		: 	05 October 2016
# Modified 		: 	05 October 2016
# Version 		: 	1.0

"""
This script used to set a user's password
"""

import random
import sys
sys.path.append("../model")

from base_handler import BaseHandler
from valid_model import is_valid_pwd
from mongoconn_model import getclient
from account_model import account_info
from account_model import set_pwd

class SetpwdHandler(BaseHandler) :

    def __init__(self,post_data,post_files,usr_session,server_conf):
        super(SetpwdHandler,self).__init__(post_data,post_files,usr_session,server_conf)

    def perform(self):
        # accept parameters
        old_pwd = self._post_data['old_pwd']
        new_pwd = self._post_data['new_pwd']
        token = int(self._post_data['token'])

        # if not login
        if 'user_id' not in self._usr_session:
            return {'result':False,'reason':1}

        # if token is wrong
        if 'token' not in self._usr_session or token != self._usr_session['token']:
            return {'result':False,'reason':2}

        # if new pwd is invalid
        if is_valid_pwd(new_pwd) is False:
            return {'result':False,'reason':3}

        # connect to mongo
        db_conn = getclient(self._server_conf['mongo']['hosts'],\
            self._server_conf['mongo']['replset'],self._server_conf['mongo']['db_name'],\
            self._server_conf['mongo']['db_user'],self._server_conf['mongo']['db_pwd'])

        # response when old pwd is wrong
        response = {'result':False,'reason':4}

        if is_valid_pwd(old_pwd) is True:
            info = account_info(db_conn,\
                self._server_conf['mongo']['db_name'],\
                self._usr_session['user_id'])
            if info is not None and old_pwd == info['password']:
                # if old pwd is right
                response['result'] = True
                response.pop('reason',None)
                # update pwd
                set_pwd(db_conn,self._server_conf['mongo']['db_name'],\
                    self._usr_session['user_id'],new_pwd)
                # produce a new token
                token = random.randint(self._server_conf['auth']['token_min'],\
                    self._server_conf['auth']['token_max'])
                self._usr_session['token'] = token

        # return result
        db_conn.close()
        return response
