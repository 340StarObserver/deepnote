#!/usr/bin/python
# -*- coding:utf-8 -*-

# Author 		: 	Lv Yang
# Created 		: 	05 October 2016
# Modified 		: 	05 October 2016
# Version 		: 	1.0

"""
This script used to logout
"""

from base_handler import BaseHandler

class LogoutHandler(BaseHandler) :

    def __init__(self,post_data,post_files,usr_session,server_conf):
        super(LogoutHandler,self).__init__(post_data,post_files,usr_session,server_conf)

    def perform(self):
        pass
