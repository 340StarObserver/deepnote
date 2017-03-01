#!/usr/bin/python
# -*- coding:utf-8 -*-

# Author 		: 	Lv Yang
# Created 		: 	05 October 2016
# Modified 		: 	13 October 2016
# Version 		: 	1.0

"""
This script used to get a note's comments sorted by time desc, page by page
"""

import sys
sys.path.append("../model")

from base_handler import BaseHandler
from mongoconn_model import getclient

class GetcommentHandler(BaseHandler) :

    def __init__(self,post_data,post_files,usr_session,server_conf):
        super(GetcommentHandler,self).__init__(post_data,post_files,usr_session,server_conf)

    def perform(self):
        # accept parameters
        note_id = self._post_data['note_id']
        ancestor_id = self._post_data['ancestor_id']
        page_id = int(self._post_data['page_id'])
        page_size = int(self._post_data['page_size'])

        response = {'comments':[]}
        if page_id > 0 and page_size > 0:
            # connect to mongo
            db_conn = getclient(self._server_conf['mongo']['hosts'],\
                self._server_conf['mongo']['replset'],self._server_conf['mongo']['db_name'],\
                self._server_conf['mongo']['db_user'],self._server_conf['mongo']['db_pwd'])
            # do query
            res = db_conn[self._server_conf['mongo']['db_name']]['comment_record'].find(\
                {'note_id':note_id,'ancestor_id':ancestor_id},\
                skip=(page_id-1)*page_size,limit=page_size)
            for comment in res:
                comment['_id'] = str(comment['_id'])
                comment['recv_ids'] = ','.join(comment['recv_ids'])
                response['comments'].append(comment)
            # disconnect
            db_conn.close()

        # return result
        return response
