#!/usr/bin/python
# -*- coding:utf-8 -*-

# Author 		: 	Lv Yang
# Created 		: 	05 October 2016
# Modified 		: 	22 October 2016
# Version 		: 	1.0

"""
This script used to get users' info who I care, sorted by time desc, page py page
"""

import sys
sys.path.append("../model")

from base_handler import BaseHandler
from mongoconn_model import getclient
from account_model import account_info

class GetcareHandler(BaseHandler) :

    def __init__(self,post_data,post_files,usr_session,server_conf):
        super(GetcareHandler,self).__init__(post_data,post_files,usr_session,server_conf)

    def perform(self):
        # accept parameters
        page_id = int(self._post_data['page_id'])
        page_size = int(self._post_data['page_size'])

        # declare response
        response = {'cares':[]}

        if page_id > 0 and page_size > 0 and 'user_id' in self._usr_session:
            # connect to mongo
            db_conn = getclient(self._server_conf['mongo']['hosts'],\
                self._server_conf['mongo']['replset'],self._server_conf['mongo']['db_name'],\
                self._server_conf['mongo']['db_user'],self._server_conf['mongo']['db_pwd'])
            # do query
            res = db_conn[self._server_conf['mongo']['db_name']]['care_record'].find(\
                {'carer_id':self._usr_session['user_id']},\
                skip=(page_id-1)*page_size,limit=page_size)
            for people in res:
                info = account_info(db_conn,self._server_conf['mongo']['db_name'],people['cared_id'])
                if info is not None:
                    info.pop('password',None)
                    response['cares'].append(info)
            # disconnect
            db_conn.close()

        # return result
        return response
