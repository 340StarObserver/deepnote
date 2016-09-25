#!/usr/bin/python
# -*- coding:utf-8 -*-

# Author 		: 	Lv Yang
# Created 		: 	24 September 2016
# Modified 		: 	24 September 2016
# Version 		: 	1.0

"""
This script defines a base handler
"""

class BaseHandler(object) :
    
    def __init__(self,post_data,post_files,usr_session,server_conf):
        """
        parameters :
            'post_data' is the POST data which not files
            'post_files' is the POST files
            'usr_session' is session of the current user
            'server_conf' is the global shared config
        """
        self._post_data = post_data
        self._post_files = post_files
        self._usr_session = usr_session
        self._server_conf = server_conf

    def perform(self):
        """
        deal with request and finally return result as a dict
        """
        return {}
