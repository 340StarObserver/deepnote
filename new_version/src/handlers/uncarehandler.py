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

from basehandler import BaseHandler


""" cancel care another """
class UncareHandler(BaseHandler):

	def __init__(self, post_data, post_files, usr_session):
		super(UncareHandler, self).__init__(post_data, post_files, usr_session)

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
			user = AppConf.get('pg', 'rw_usr'), \
			password = AppConf.get('pg', 'rw_pwd'), \
			database = "dp_note")
		pg_cursor = pg_conn.cursor()
		pg_cursor.execute("delete from usercare where usr_id=%s and care_nick=%s", \
			(self._usr_session['usr_id'], care_nick))
		pg_conn.commit()
		pg_conn.close()

		# return result
		return {'result' : True}
