#!/usr/bin/python
# -*- coding:utf-8 -*-

# Author 		: 	Lv Yang
# Created 		: 	24 September 2016
# Modified 		: 	24 September 2016
# Version 		: 	1.0

"""
This script defines a factory which produces different kinds of handlers
"""

from base_handler import BaseHandler
from verifycode_handler import VerifycodeHandler

class HandlerFactory :
    @staticmethod
    def produce(action_id,post_data,post_files,usr_session,server_conf):
        """
        produce a corresponding handler based on the action_id
        parameters :
            'post_data' is the POST data which not files
            'post_files' is the POST files
            'usr_session' is session of the current user
            'server_conf' is the global shared config
        """
        try:
            action_id = int(action_id)
        except:
            action_id = 0
        if action_id is 101:
            return VerifycodeHandler(post_data,post_files,usr_session,server_conf)
        return BaseHandler(post_data,post_files,usr_session,server_conf)
