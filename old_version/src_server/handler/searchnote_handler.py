#!/usr/bin/python
# -*- coding:utf-8 -*-

# Author 		: 	Lv Yang
# Created 		: 	05 October 2016
# Modified 		: 	22 October 2016
# Version 		: 	1.0

"""
This script used to search notes by given a sentence
"""

import sys
sys.path.append("../model")

from base_handler import BaseHandler
from search_model import fuzzySearch
from search_model import note_baseinfo
import mongoconn_model
import esconn_model


class SearchnoteHandler(BaseHandler) :

    def __init__(self,post_data,post_files,usr_session,server_conf):
        super(SearchnoteHandler,self).__init__(post_data,post_files,usr_session,server_conf)

    def perform(self):
        # accept parameters
        sentence = self._post_data['sentence']
        page_id = int(self._post_data['page_id'])
        page_size = int(self._post_data['page_size'])

        # declare response
        response = {'notes':[]}
        if len(sentence) > 0 and page_id > 0 and page_size > 0:
            # connect to mongo
            db_conn = mongoconn_model.getclient(self._server_conf['mongo']['hosts'],\
                self._server_conf['mongo']['replset'],self._server_conf['mongo']['db_name'],\
                self._server_conf['mongo']['db_user'],self._server_conf['mongo']['db_pwd'])
            # connect to elasticsearch
            es_conn = esconn_model.getclient(self._server_conf['elasticsearch']['hosts'])
            # do query
            note_ids = fuzzySearch(es_conn,\
                self._server_conf['elasticsearch']['index'],\
                self._server_conf['elasticsearch']['type'],\
                sentence,page_id,page_size)
            for note_id in note_ids:
                info = note_baseinfo(db_conn,self._server_conf['mongo']['db_name'],note_id)
                if info is not None:
                    response['notes'].append(info)
            # disconnect
            db_conn.close()

        # return result
        return response
