#!/usr/bin/python
# -*- coding:utf-8 -*-

# Author 		: 	Lv Yang
# Created 		: 	04 March 2017
# Modified 		: 	04 March 2017
# Version 		: 	1.0

import psycopg2

import sys
sys.path.append("../common")

from appconf import AppConf
from appvalid import AppValid

from basehandler import BaseHandler


""" set a user's signature """
class SignatureHandler(BaseHandler):

	def __init__(self, post_data, post_files, usr_session):
		super(SignatureHandler, self).__init__(post_data, post_files, usr_session)

	def perform(self):
		# if not login
		if 'usr_id' not in self._usr_session:
			return {'result' : False, 'reason' : 1}

		# if signature is invalid
		sign = self._post_data['signature']
		if AppValid.validSignature(sign) is False:
			return {'result' : False, 'reason' : 2}

		# conn to pg
		pg_conn = psycopg2.connect(\
			host = AppConf.get('pg', 'host'), \
			port = AppConf.get('pg', 'port'), \
			user = AppConf.get('pg', 'rw_usr'), \
			password = AppConf.get('pg', 'rw_pwd'), \
			database = "dp_note")
		pg_cursor = pg_conn.cursor()
		pg_cursor.execute("update userinfo set signature=%s where usr_id=%s", \
			(sign, self._usr_session['usr_id']))
		pg_conn.commit()
		pg_conn.close()

		# return result
		return {'result' : True}
