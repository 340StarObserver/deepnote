#!/usr/bin/python
# -*- coding:utf-8 -*-

# Author 		: 	Lv Yang
# Created 		: 	05 October 2016
# Modified 		: 	12 October 2016
# Version 		: 	1.0

"""
This script used to get a note's detail information
"""

import sys
sys.path.append("../model")

from base_handler import BaseHandler
from mongoconn_model import getclient
from search_model import note_detailinfo

class NotedetailHandler(BaseHandler) :

    def __init__(self,post_data,post_files,usr_session,server_conf):
        super(NotedetailHandler,self).__init__(post_data,post_files,usr_session,server_conf)

    def perform(self):
        # connect to mongo
        db_conn = getclient(self._server_conf['mongo']['hosts'],\
            self._server_conf['mongo']['replset'],self._server_conf['mongo']['db_name'],\
            self._server_conf['mongo']['db_user'],self._server_conf['mongo']['db_pwd'])
        # do query
        response = {'result':False}
        note = note_detailinfo(db_conn,self._server_conf['mongo']['db_name'],self._post_data['note_id'])
        if note is not None:
            response = note
            response['result'] = True
        # return result
        db_conn.close()
        return response
