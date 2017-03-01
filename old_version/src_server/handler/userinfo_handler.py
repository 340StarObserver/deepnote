#!/usr/bin/python
# -*- coding:utf-8 -*-

# Author 		: 	Lv Yang
# Created 		: 	05 October 2016
# Modified 		: 	11 October 2016
# Version 		: 	1.0

"""
This script used to get a user's info
"""

import sys
sys.path.append("../model")

from base_handler import BaseHandler
from valid_model import is_valid_phone
from mongoconn_model import getclient
from account_model import account_info

class UserinfoHandler(BaseHandler) :

    def __init__(self,post_data,post_files,usr_session,server_conf):
        super(UserinfoHandler,self).__init__(post_data,post_files,usr_session,server_conf)

    def perform(self):
        # if usr is invalid
        usr = self._post_data['usr']
        if is_valid_phone(usr) is False:
            return {'result':False}

        # connect to mongo
        db_conn = getclient(self._server_conf['mongo']['hosts'],\
            self._server_conf['mongo']['replset'],self._server_conf['mongo']['db_name'],\
            self._server_conf['mongo']['db_user'],self._server_conf['mongo']['db_pwd'])

        response = None
        info = account_info(db_conn,self._server_conf['mongo']['db_name'],usr)
        if info is None:
            # this usr not exist
            response = {'result':False}
        else:
            # this usr exists
            info.pop('password',None)
            response = info
            response['result'] = True

        # return result
        db_conn.close()
        return response
