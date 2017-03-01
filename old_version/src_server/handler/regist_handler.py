#!/usr/bin/python
# -*- coding:utf-8 -*-

# Author 		: 	Lv Yang
# Created 		: 	05 October 2016
# Modified 		: 	05 October 2016
# Version 		: 	1.0

"""
This script used to regist a new account
"""

import time
import sys
sys.path.append("../model")

from base_handler import BaseHandler
from valid_model import is_valid_phone
from valid_model import is_valid_pwd
from valid_model import is_valid_nick
from mongoconn_model import getclient
from account_model import exist_account

class RegistHandler(BaseHandler) :

    def __init__(self,post_data,post_files,usr_session,server_conf):
        super(RegistHandler,self).__init__(post_data,post_files,usr_session,server_conf)

    def perform(self):
        # accept parameters
        usr = self._post_data['usr']
        pwd = self._post_data['pwd']
        nick = self._post_data['nick']
        code = int(self._post_data['code'])

        # if verifycode is wrong
        timestamp = int(time.time())
        if 'verify_code' not in self._usr_session or 'verify_time' not in self._usr_session or \
            timestamp - self._usr_session['verify_time'] > self._server_conf['sms']['time_limit'] or \
            code != self._usr_session['verify_code']:
            return {'result':False,'reason':1}

        # if usr or pwd is invalid
        if is_valid_phone(usr) is False or is_valid_pwd(pwd) is False:
            return {'result':False,'reason':2}

        # if nick is invalid
        if is_valid_nick(nick) is False:
            return {'result':False,'reason':3}

        # connect to mongo
        db_conn = getclient(self._server_conf['mongo']['hosts'],\
            self._server_conf['mongo']['replset'],self._server_conf['mongo']['db_name'],\
            self._server_conf['mongo']['db_user'],self._server_conf['mongo']['db_pwd'])

        response = {'result':True}
        if exist_account(db_conn,self._server_conf['mongo']['db_name'],usr) is True:
            # if this account already exists
            response['result'] = False
            response['reason'] = 4
        else:
            # add this new account to mongo
            doc = {}
            doc['_id'] = usr
            doc['password'] = pwd
            doc['nick'] = nick
            doc['signup_time'] = timestamp
            doc['signature'] = ""
            db_conn[self._server_conf['mongo']['db_name']]['user_info'].insert_one(doc)

        # return result
        db_conn.close()
        return response
