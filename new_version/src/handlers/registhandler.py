#!/usr/bin/python
# -*- coding:utf-8 -*-

# Author 		: 	Lv Yang
# Created 		: 	02 March 2017
# Modified 		: 	02 March 2017
# Version 		: 	1.0

import time
import psycopg2

import sys
sys.path.append("../common")

from appconf import AppConf
from appvalid import AppValid
from applogger import AppLogger

from basehandler import BaseHandler


""" regist a new account """
class RegistHandler(BaseHandler):

	def __init__(self, post_data, post_files, usr_session):
		super(RegistHandler, self).__init__(post_data, post_files, usr_session)

	def perform(self):
		# receive parameters
		usr_id = self._post_data['usr_id']
		usr_pwd = self._post_data['usr_pwd']
		usr_nick = self._post_data['usr_nick']
		code = int(self._post_data['code'])

		# if verify code is wrong
		if 'verify_code' not in self._usr_session or 'verify_time' not in self._usr_session or \
			int(time.time()) - self._usr_session['verify_time'] > AppConf.get('sms', 'time_limit') or \
			code != self._usr_session['verify_code']:
			return {'result' : False, 'reason' : 1}

		# if usr_id or usr_pwd is invalid
		if AppValid.validPhone(usr_id) is False or AppValid.validPasswd(usr_pwd) is False:
			return {'result' : False, 'reason' : 2}

		# if usr_nick is invalid
		if AppValid.validNick(usr_nick) is False:
			return {'result' : False, 'reason' : 3}

		# conn to pg
		pg_conn = psycopg2.connect(\
			host = AppConf.get('pg_rw', 'host'), \
			port = AppConf.get('pg_rw', 'port'), \
			user = AppConf.get('pg_rw', 'usr'), \
			password = AppConf.get('pg_rw', 'pwd'), \
			database = "dp_note")
		pg_cursor = pg_conn.cursor()
		try:
			pg_cursor.execute("insert into userinfo (usr_id, usr_nick, usr_pwd) values (%s, %s, %s)", \
				(int(usr_id), usr_nick, usr_pwd))
			pg_conn.commit()
			response = {'result' : True}
		except Exception, e:
			AppLogger.getInstance().error(str(e))
			AppLogger.getInstance().info("[phone:%s] [nick:%s] AlreadyExist" % (usr_id, usr_nick))
			response = {'result' : False, 'reason' : 4}
		finally:
			pg_conn.close()

		# return result
		return response
