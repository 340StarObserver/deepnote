#!/usr/bin/python
# -*- coding:utf-8 -*-

# Author 		: 	Lv Yang
# Created 		: 	05 October 2016
# Modified 		: 	21 October 2016
# Version 		: 	1.0

"""
This script used to get my collections sorted by time desc, page py page
"""

import sys
sys.path.append("../model")

from base_handler import BaseHandler
from mongoconn_model import getclient
from search_model import note_baseinfo

class GetcollectHandler(BaseHandler) :

    def __init__(self,post_data,post_files,usr_session,server_conf):
        super(GetcollectHandler,self).__init__(post_data,post_files,usr_session,server_conf)

    def perform(self):
        # accept parameters
        page_id = int(self._post_data['page_id'])
        page_size = int(self._post_data['page_size'])

        # declare response
        response = {'notes':[]}

        if page_id > 0 and page_size > 0 and 'user_id' in self._usr_session:
            # connect to mongo
            db_conn = getclient(self._server_conf['mongo']['hosts'],\
                self._server_conf['mongo']['replset'],self._server_conf['mongo']['db_name'],\
                self._server_conf['mongo']['db_user'],self._server_conf['mongo']['db_pwd'])
            # do query
            notes = db_conn[self._server_conf['mongo']['db_name']]['note_collect'].find(\
                {'user_id':self._usr_session['user_id']},{'_id':0,'note_id':1},\
                skip=(page_id-1)*page_size,limit=page_size)
            for note in notes:
                info = note_baseinfo(db_conn,self._server_conf['mongo']['db_name'],note['note_id'])
                if info is not None:
                    response['notes'].append(info)
            # disconnect
            db_conn.close()

        # return result
        return response
