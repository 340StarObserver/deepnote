#!/usr/bin/python
# -*- coding:utf-8 -*-

# Author 		: 	Lv Yang
# Created 		: 	05 October 2016
# Modified 		: 	11 October 2016
# Version 		: 	1.0

"""
This script used to login
"""

import random
import sys
sys.path.append("../model")

from base_handler import BaseHandler
from valid_model import is_valid_phone
from valid_model import is_valid_pwd
from mongoconn_model import getclient
from account_model import account_info

class LoginHandler(BaseHandler) :

    def __init__(self,post_data,post_files,usr_session,server_conf):
        super(LoginHandler,self).__init__(post_data,post_files,usr_session,server_conf)

    def perform(self):
        # accept parameters
        usr = self._post_data['usr']
        pwd = self._post_data['pwd']

        # if usr or pwd is invalid
        if is_valid_phone(usr) is False or is_valid_pwd(pwd) is False:
            return {'result':False,'reason':1}

        # connect to mongo
        db_conn = getclient(self._server_conf['mongo']['hosts'],\
            self._server_conf['mongo']['replset'],self._server_conf['mongo']['db_name'],\
            self._server_conf['mongo']['db_user'],self._server_conf['mongo']['db_pwd'])

        response = {'result':True}
        info = account_info(db_conn,self._server_conf['mongo']['db_name'],usr)
        if info is None:
            # if this usr not exist
            response['result'] = False
            response['reason'] = 2
        elif info['password'] != pwd:
            # if password is wrong
            response['result'] = False
            response['reason'] = 3
        else:
            # login success
            response['nick'] = info['nick']
            response['signup_time'] = info['signup_time']
            response['signature'] = info['signature']
            # create a token
            token = random.randint(self._server_conf['auth']['token_min'],\
                self._server_conf['auth']['token_max'])
            response['token'] = token
            # save session
            self._usr_session['token'] = token
            self._usr_session['user_id'] = info['_id']
            self._usr_session['nick'] = info['nick']

        # return result
        db_conn.close()
        return response
