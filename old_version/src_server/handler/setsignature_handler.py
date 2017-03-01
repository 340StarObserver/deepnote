#!/usr/bin/python
# -*- coding:utf-8 -*-

# Author 		: 	Lv Yang
# Created 		: 	05 October 2016
# Modified 		: 	05 October 2016
# Version 		: 	1.0

"""
This script used to set a user's signature
"""

import sys
sys.path.append("../model")

from base_handler import BaseHandler
from mongoconn_model import getclient
from account_model import account_info

class SetsignatureHandler(BaseHandler) :

    def __init__(self,post_data,post_files,usr_session,server_conf):
        super(SetsignatureHandler,self).__init__(post_data,post_files,usr_session,server_conf)

    def perform(self):
        # if not login
        if 'user_id' not in self._usr_session:
            return {'result':False,'reason':1}

        signature = self._post_data['signature']
        # connect to mongo
        db_conn = getclient(self._server_conf['mongo']['hosts'],\
            self._server_conf['mongo']['replset'],self._server_conf['mongo']['db_name'],\
            self._server_conf['mongo']['db_user'],self._server_conf['mongo']['db_pwd'])

        # update signature
        factor_1 = {'_id':self._usr_session['user_id']}
        factor_2 = {'$set':{'signature':signature}}
        db_conn[self._server_conf['mongo']['db_name']]['user_info'].update_one(factor_1,factor_2)

        # return result
        db_conn.close()
        return {'result':True}
