#!/usr/bin/python
# -*- coding:utf-8 -*-

# Author 		: 	Lv Yang
# Created 		: 	19 March 2017
# Modified 		: 	19 March 2017
# Version 		: 	1.0

import random
import psycopg2

import sys
sys.path.append("../common")

from appconf import AppConf
from appvalid import AppValid
from applogger import AppLogger

from basehandler import BaseHandler


""" update a note """
class UpdatenoteHandler(BaseHandler):

	def __init__(self, post_data, post_files, usr_session):
		super(UpdatenoteHandler, self).__init__(post_data, post_files, usr_session)

	def perform(self):
		# if not login
		if 'usr_id' not in self._usr_session:
			return {'result' : False, 'reason' : 1}

		# if token is wrong
		token = int(self._post_data['token'])
		if 'token' not in self._usr_session or token != self._usr_session['token']:
			return {'result' : False, 'reason' : 2}

		# receive parameters
		note_id = self._post_data['note_id']
		tags = self._post_data['tags']
		refs = self._post_data['refs']
		feel = self._post_data['feel']

		# if note's feel invalid
		if AppValid.validNoteFeel(feel) is False:
			return {'result' : False, 'reason' : 3}

		# conn to pg
		pg_conn = psycopg2.connect(\
			host = AppConf.get('pg', 'host'), \
			port = AppConf.get('pg', 'port'), \
			user = AppConf.get('pg', 'rw_usr'), \
			password = AppConf.get('pg', 'rw_pwd'), \
			database = "dp_note")

		# try to update
		try:
			pg_cursor = pg_conn.cursor()
			pg_cursor.execute("select updatenote(%s, %s, %s, %s, %s)", \
				(note_id, self._usr_session['usr_nick'], tags, refs, feel))
			pg_conn.commit()
		except Exception, e:
			AppLogger.getInstance().error(str(e))
			pg_conn.rollback()
		finally:
			pg_conn.close()

		# create a new token
		token = random.randint(AppConf.get('auth', 'token_min'), AppConf.get('auth', 'token_max'))
		self._usr_session['token'] = token

		# return result
		return {'result' : True, 'token' : token}
