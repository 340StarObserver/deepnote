#!/usr/bin/python
# -*- coding:utf-8 -*-

# Author 		: 	Lv Yang
# Created 		: 	05 October 2016
# Modified 		: 	12 October 2016
# Version 		: 	1.0

"""
This script used to query notes sorted by time desc, page by page
"""

import sys
sys.path.append("../model")

from base_handler import BaseHandler
from mongoconn_model import getclient

class GetnotebytimeHandler(BaseHandler) :

    def __init__(self,post_data,post_files,usr_session,server_conf):
        super(GetnotebytimeHandler,self).__init__(post_data,post_files,usr_session,server_conf)

    def perform(self):
        # accept parameters
        page_size = int(self._post_data['page_size'])
        time_max = int(self._post_data['time_max'])

        response = {'notes':[]}
        if page_size > 0 and time_max > 0:
            # do query
            db_conn = getclient(self._server_conf['mongo']['hosts'],\
                self._server_conf['mongo']['replset'],self._server_conf['mongo']['db_name'],\
                self._server_conf['mongo']['db_user'],self._server_conf['mongo']['db_pwd'])
            notes = db_conn[self._server_conf['mongo']['db_name']]['note_base'].find(\
                {'pub_time':{'$lt':time_max}},limit=page_size)
            for note in notes:
                note['_id'] = str(note['_id'])
                response['notes'].append(note)
            db_conn.close()

        # return result
        return response
