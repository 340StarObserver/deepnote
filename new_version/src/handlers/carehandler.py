#!/usr/bin/python
# -*- coding:utf-8 -*-

# Author 		: 	Lv Yang
# Created 		: 	05 March 2017
# Modified 		: 	05 March 2017
# Version 		: 	1.0

import psycopg2

import sys
sys.path.append("../common")

from appconf import AppConf
from appvalid import AppValid
from applogger import AppLogger

from basehandler import BaseHandler


""" care another """
class CareHandler(BaseHandler):

	def __init__(self, post_data, post_files, usr_session):
		super(CareHandler, self).__init__(post_data, post_files, usr_session)

	def perform(self):
		# if not login
		if 'usr_id' not in self._usr_session:
			return {'result' : False, 'reason' : 1}

		# if care_nick is invalid
		care_nick = self._post_data['care_nick']
		if AppValid.validNick(care_nick) is False:
			return {'result' : False, 'reason' : 2}

		# conn to pg
		pg_conn = psycopg2.connect(\
			host = AppConf.get('pg', 'host'), \
			port = AppConf.get('pg', 'port'), \
			user = AppConf.get('pg', 'w_usr'), \
			password = AppConf.get('pg', 'w_pwd'), \
			database = "dp_note")
		pg_cursor = pg_conn.cursor()
		try:
			pg_cursor.execute("insert into usercare (usr_id, care_nick) values (%s, %s)", \
				(self._usr_session['usr_id'], care_nick))
			pg_conn.commit()
			response = {'result' : True}
		except Exception, e:
			AppLogger.getInstance().error(str(e))
			response = {'result' : False, 'reason' : 3}
		finally:
			pg_conn.close()

		# return result
		return response
