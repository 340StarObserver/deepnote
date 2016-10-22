#!/usr/bin/python
# -*- coding:utf-8 -*-

# Author 		: 	Lv Yang
# Created 		: 	05 October 2016
# Modified 		: 	05 October 2016
# Version 		: 	1.0

"""
This script used to get messages about me, sorted by time desc, page py page
"""

import sys
sys.path.append("../model")

from base_handler import BaseHandler
from mongoconn_model import getclient

class MessageHandler(BaseHandler) :

    def __init__(self,post_data,post_files,usr_session,server_conf):
        super(MessageHandler,self).__init__(post_data,post_files,usr_session,server_conf)

    def perform(self):
        # accept parameters
        page_id = int(self._post_data['page_id'])
        page_size = int(self._post_data['page_size'])

        # declare response
        response = {'messages':[]}

        if page_id > 0 and page_size > 0 and 'user_id' in self._usr_session:
            # connect to mongo
            db_conn = getclient(self._server_conf['mongo']['hosts'],\
                self._server_conf['mongo']['replset'],self._server_conf['mongo']['db_name'],\
                self._server_conf['mongo']['db_user'],self._server_conf['mongo']['db_pwd'])
            # do query
            res = db_conn[self._server_conf['mongo']['db_name']]['message_record'].find(\
                {'user_ids':self._usr_session['user_id']},\
                {'_id':0,'user_ids':0},\
                skip=(page_id-1)*page_size,limit=page_size)
            for msg in res:
                response['messages'].append(msg)
            # disconnect
            db_conn.close()

        # return result
        return response
