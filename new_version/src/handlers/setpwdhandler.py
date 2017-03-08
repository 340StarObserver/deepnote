#!/usr/bin/python
# -*- coding:utf-8 -*-

# Author 		: 	Lv Yang
# Created 		: 	05 March 2017
# Modified 		: 	05 March 2017
# Version 		: 	1.0

import random
import psycopg2

import sys
sys.path.append("../common")

from appconf import AppConf
from appvalid import AppValid

from basehandler import BaseHandler


""" reset pwd when known the old pwd """
class SetpwdHandler(BaseHandler):

	def __init__(self, post_data, post_files, usr_session):
		super(SetpwdHandler, self).__init__(post_data, post_files, usr_session)

	def perform(self):
		# if not login
		if 'usr_id' not in self._usr_session:
			return {'result' : False, 'reason' : 1}

		# if token is wrong
		token = int(self._post_data['token'])
		if 'token' not in self._usr_session or token != self._usr_session['token']:
			return {'result' : False, 'reason' : 2}

		# pwd is invalid
		old_pwd = self._post_data['old_pwd']
		new_pwd = self._post_data['new_pwd']
		if AppValid.validPasswd(old_pwd) is False or AppValid.validPasswd(new_pwd) is False:
			return {'result' : False, 'reason' : 3}

		# conn to pg
		pg_conn = psycopg2.connect(\
			host = AppConf.get('pg', 'host'), \
			port = AppConf.get('pg', 'port'), \
			user = AppConf.get('pg', 'rw_usr'), \
			password = AppConf.get('pg', 'rw_pwd'), \
			database = "dp_note")
		pg_cursor = pg_conn.cursor()
		pg_cursor.execute("update userinfo set usr_pwd=%s where usr_id=%s and usr_pwd=%s", \
			(new_pwd, self._usr_session['usr_id'], old_pwd))
		pg_conn.commit()
		rows = pg_cursor.rowcount
		pg_conn.close()

		# return result
		if rows == 0:
			return {'result' : False, 'reason' : 4}
		else:
			token = random.randint(AppConf.get('auth', 'token_min'), AppConf.get('auth', 'token_max'))
			self._usr_session['token'] = token
			return {'result' : True, 'token' : token}
