#!/usr/bin/python
# -*- coding:utf-8 -*-

# Author 		: 	Lv Yang
# Created 		: 	02 March 2017
# Modified 		: 	02 March 2017
# Version 		: 	1.0

import random
import psycopg2

import sys
sys.path.append("../common")

from appconf import AppConf
from appvalid import AppValid

from basehandler import BaseHandler

class LoginHandler(BaseHandler):

	def __init__(self, post_data, post_files, usr_session):
		super(LoginHandler, self).__init__(post_data, post_files, usr_session)

	def perform(self):
		# receive parameters
		usr_id = self._post_data['usr_id']
		usr_pwd = self._post_data['usr_pwd']

		# if usr_id or usr_pwd is invalid
		if AppValid.validPhone(usr_id) is False or AppValid.validPasswd(usr_pwd) is False:
			return {'result' : False, 'reason' : 1}

		# conn to pg
		pg_conn = psycopg2.connect(\
			host = AppConf.get('pg_r', 'host'), \
			port = AppConf.get('pg_r', 'port'), \
			user = AppConf.get('pg_r', 'usr'), \
			password = AppConf.get('pg_r', 'pwd'), \
			database = "dp_note")
		pg_cursor = pg_conn.cursor()
		pg_cursor.execute(\
			"select usr_id,usr_nick,regist_time,signature from userinfo where usr_id=%s and usr_pwd=%s limit 1", \
			(int(usr_id), usr_pwd))
		usr_info = pg_cursor.fetchone()
		pg_conn.close()

		# if not found
		if usr_info is None:
			response = {'result' : False, 'reason' : 2}
		else:
			# create a token
			token = random.randint(AppConf.get('auth', 'token_min'), AppConf.get('auth', 'token_max'))
			# create session
			self._usr_session['usr_id'] = usr_info[0]
			self._usr_session['usr_nick'] = usr_info[1]
			self._usr_session['token'] = token
			# create response
			response = {
				'result' : True,
				'usr_id' : usr_info[0],
				'regist_time' : str(usr_info[2]),
				'signature' : usr_info[3],
				'token' : token
			}

		# return result
		return response
