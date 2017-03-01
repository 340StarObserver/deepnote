#!/usr/bin/python
# -*- coding:utf-8 -*-

# Author 		: 	Lv Yang
# Created 		: 	05 October 2016
# Modified 		: 	12 October 2016
# Version 		: 	1.0

"""
This script used to reset password when forget the original password
"""

import time
import random
import sys
sys.path.append("../model")

from base_handler import BaseHandler
from valid_model import is_valid_phone
from valid_model import is_valid_pwd
from mongoconn_model import getclient
from account_model import exist_account
from account_model import set_pwd

class ForgetpwdHandler(BaseHandler) :

    def __init__(self,post_data,post_files,usr_session,server_conf):
        super(ForgetpwdHandler,self).__init__(post_data,post_files,usr_session,server_conf)

    def perform(self):
        # accept parameters
        usr = self._post_data['usr']
        pwd = self._post_data['pwd']
        code = int(self._post_data['code'])

        # if verifycode is wrong
        timestamp = int(time.time())
        if 'verify_code' not in self._usr_session or 'verify_time' not in self._usr_session or \
            timestamp - self._usr_session['verify_time'] > self._server_conf['sms']['time_limit'] or \
            code != self._usr_session['verify_code']:
            return {'result':False,'reason':1}

        # if new pwd is invalid
        if is_valid_pwd(pwd) is False:
            return {'result':False,'reason':2}

        # connect to mongo
        db_conn = getclient(self._server_conf['mongo']['hosts'],\
            self._server_conf['mongo']['replset'],self._server_conf['mongo']['db_name'],\
            self._server_conf['mongo']['db_user'],self._server_conf['mongo']['db_pwd'])

        response = {'result':True}
        if is_valid_phone(usr) is False or exist_account(db_conn,self._server_conf['mongo']['db_name'],usr) is None:
            # if this usr not exist
            response['result'] = False
            response['reason'] = 3
        else:
            # if this usr exists
            set_pwd(db_conn,self._server_conf['mongo']['db_name'],usr,pwd)

        # return result
        db_conn.close()
        return response
