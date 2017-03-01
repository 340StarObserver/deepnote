#!/usr/bin/python
# -*- coding:utf-8 -*-

# Author 		: 	Lv Yang
# Created 		: 	01 March 2017
# Modified 		: 	01 March 2017
# Version 		: 	1.0

import urllib2
import random
import time
import re

import sys
sys.path.append("../common")

from appconf import AppConf
from appvalid import AppValid

from basehandler import BaseHandler


""" send verify code by sms """
class SmsHandler(BaseHandler) :

	def __init__(self, post_data, post_files, usr_session):
		super(SmsHandler, self).__init__(post_data, post_files, usr_session)

	def perform(self):
		# if phone is invalid
		phone = self._post_data['phone']
		if AppValid.validPhone(phone) == False:
			return {'result' : False, 'reason' : 1}

		# create a verify code and save it to session
		code = random.randint(AppConf.get('sms', 'code_min'), AppConf.get('sms', 'code_max'))
		self._usr_session['verify_code'] = code
		self._usr_session['verify_time'] = int(time.time())

		# send verify code to user by sms
		# send verify code to user by sms
		request_url = AppConf.get('sms', 'url')%(\
			AppConf.get('sms', 'access_key'), \
			AppConf.get('sms', 'secret_key'), \
			phone, phone, code)
		req = urllib2.Request(request_url)
		urllib2.urlopen(req)

		# return result
		return {'result' : True}
