#!/usr/bin/python
# -*- coding:utf-8 -*-

# Author 		: 	Lv Yang
# Created 		: 	05 March 2017
# Modified 		: 	05 March 2017
# Version 		: 	1.0

import time
import psycopg2

import sys
sys.path.append("../common")

from appconf import AppConf
from appvalid import AppValid

from basehandler import BaseHandler

""" reset a user's pwd when forget the old pwd """
class ForgetpwdHandler(BaseHandler):

	def __init__(self, post_data, post_files, usr_session):
		super(ForgetpwdHandler, self).__init__(post_data, post_files, usr_session)

	def perform(self):
		# receive parameters
		usr_id = self._post_data['usr_id']
		usr_pwd = self._post_data['usr_pwd']
		code = int(self._post_data['code'])

		# if verify code is wrong
		if 'verify_code' not in self._usr_session or 'verify_time' not in self._usr_session or \
			int(time.time()) - self._usr_session['verify_time'] > AppConf.get('sms', 'time_limit') or \
			code != self._usr_session['verify_code']:
			return {'result' : False, 'reason' : 1}

		# if usr_id or usr_pwd is invalid
		if AppValid.validPhone(usr_id) is False or AppValid.validPasswd(usr_pwd) is False:
			return {'result' : False, 'reason' : 2}

		# conn to pg
		pg_conn = psycopg2.connect(\
			host = AppConf.get('pg', 'host'), \
			port = AppConf.get('pg', 'port'), \
			user = AppConf.get('pg', 'rw_usr'), \
			password = AppConf.get('pg', 'rw_pwd'), \
			database = "dp_note")
		pg_cursor = pg_conn.cursor()
		pg_cursor.execute("update userinfo set usr_pwd=%s where usr_id=%s", \
			(usr_pwd, usr_id))
		pg_conn.commit()
		pg_conn.close()

		# return result
		return {'result' : True}
