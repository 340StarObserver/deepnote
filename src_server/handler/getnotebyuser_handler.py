#!/usr/bin/python
# -*- coding:utf-8 -*-

# Author 		: 	Lv Yang
# Created 		: 	05 October 2016
# Modified 		: 	12 October 2016
# Version 		: 	1.0

"""
This script used to query a user's notes page by page
"""

import sys
sys.path.append("../model")

from base_handler import BaseHandler
from valid_model import is_valid_phone
from mongoconn_model import getclient

class GetnotebyuserHandler(BaseHandler) :

    def __init__(self,post_data,post_files,usr_session,server_conf):
        super(GetnotebyuserHandler,self).__init__(post_data,post_files,usr_session,server_conf)

    def perform(self):
        # accept parameters
        who_usr = self._post_data['who_usr']
        page_id = int(self._post_data['page_id'])
        page_size = int(self._post_data['page_size'])

        # declare response
        response = {'notes':[]}
        if is_valid_phone(who_usr) is True and page_id >=0 and page_size > 0:
            # connect to mongo
            db_conn = getclient(self._server_conf['mongo']['hosts'],\
                self._server_conf['mongo']['replset'],self._server_conf['mongo']['db_name'],\
                self._server_conf['mongo']['db_user'],self._server_conf['mongo']['db_pwd'])
            # do search
            res = db_conn[self._server_conf['mongo']['db_name']]['note_base'].find({'own_id':who_usr},\
                skip=(page_id-1)*page_size,limit=page_size)
            for note in res:
                note['_id'] = str(note['_id'])
                response['notes'].append(note)
            # disconnect mongo
            db_conn.close()

        # return result
        return response
