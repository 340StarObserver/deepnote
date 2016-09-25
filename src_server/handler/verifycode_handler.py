#!/usr/bin/python
# -*- coding:utf-8 -*-

# Author 		: 	Lv Yang
# Created 		: 	24 September 2016
# Modified 		: 	25 September 2016
# Version 		: 	1.0

"""
This script used to send verify code to user by the way of mobile message
"""

import urllib2
import random
import time
import sys
sys.path.append("../model")

from base_handler import BaseHandler
from valid_model import is_valid_phone

class VerifycodeHandler(BaseHandler) :
    
    def __init__(self,post_data,post_files,usr_session,server_conf):
        super(VerifycodeHandler,self).__init__(post_data,post_files,usr_session,server_conf)

    def perform(self):
        # if phone is not valid
        phone_number = self._post_data['phone']
        if is_valid_phone(phone_number) is False:
            return {'result':False,'reason':1}

        # create a verify code and save it to session
        code = random.randint(self._server_conf['sms']['code_min'],self._server_conf['sms']['code_max'])
        self._usr_session['verify_code'] = code
        self._usr_session['verify_time'] = int(time.time())

        # send verify code to user by sms
        request_url = self._server_conf['sms']['url']%(\
            self._server_conf['sms']['access_key'],\
            self._server_conf['sms']['secret_key'],\
            phone_number,phone_number,code)
        req = urllib2.Request(request_url)
        urllib2.urlopen(req)

        # return result
        return {'result':True}
