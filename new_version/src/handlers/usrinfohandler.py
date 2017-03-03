#!/usr/bin/python
# -*- coding:utf-8 -*-

# Author 		: 	Lv Yang
# Created 		: 	03 March 2017
# Modified 		: 	03 March 2017
# Version 		: 	1.0

import psycopg2

import sys
sys.path.append("../common")

from appconf import AppConf
from appvalid import AppValid

from basehandler import BaseHandler


""" get a user's base info """
class UsrinfoHandler(BaseHandler):

	def __init__(self, post_data, post_files, usr_session):
		super(UsrinfoHandler, self).__init__(post_data, post_files, usr_session)

	def perform(self):
		# if usr_nick is invalid
		usr_nick = self._post_data['usr_nick']
		if AppValid.validNick(usr_nick) is False:
			return {'result' : False}

		# conn to pg
		pg_conn = psycopg2.connect(\
			host = AppConf.get('pg_r', 'host'), \
			port = AppConf.get('pg_r', 'port'), \
			user = AppConf.get('pg_r', 'usr'), \
			password = AppConf.get('pg_r', 'pwd'), \
			database = "dp_note")
		pg_cursor = pg_conn.cursor()
		pg_cursor.execute("select regist_time,signature from userinfo where usr_nick=%s limit 1", (usr_nick,))
		usr_info = pg_cursor.fetchone()
		pg_conn.close()

		# return result
		if usr_info is None:
			response = {'result' : False}
		else:
			response = {
				'result' : True,
				'usr_nick' : usr_nick,
				'regist_time' : str(usr_info[0]),
				'signature' : usr_info[1]
			}
		return response
