#!/usr/bin/python
# -*- coding:utf-8 -*-

# Author 		: 	Lv Yang
# Created 		: 	18 March 2017
# Modified 		: 	18 March 2017
# Version 		: 	1.0

import psycopg2

import sys
sys.path.append("../common")

from appconf import AppConf
from appvalid import AppValid

from basehandler import BaseHandler


""" query somebody's notes by page """
class NotelistHandler(BaseHandler):

	def __init__(self, post_data, post_files, usr_session):
		super(NotelistHandler, self).__init__(post_data, post_files, usr_session)

	def perform(self):
		# receive parameters
		usr_nick = self._post_data['usr_nick']
		page_id = int(self._post_data['page_id'])
		page_size = int(self._post_data['page_size'])

		# if invalid parameters
		if page_id <= 0 or page_size <= 0 or AppValid.validNick(usr_nick) is False:
			return {'result' : False}

		# conn to pg
		pg_conn = psycopg2.connect(\
			host = AppConf.get('pg', 'host'), \
			port = AppConf.get('pg', 'port'), \
			user = AppConf.get('pg', 'r_usr'), \
			password = AppConf.get('pg', 'r_pwd'), \
			database = "dp_note")
		pg_cursor = pg_conn.cursor()

		# do query
		pg_cursor.execute(\
			"select note_base.note_id, note_base.usr_nick, note_base.pub_time, note_text.title, note_text.tags \
				from note_base, note_text \
				where note_base.usr_nick=%s and note_base.note_id=note_text.note_id \
				order by note_base.pub_time desc limit %s offset %s", \
			(usr_nick, page_size, (page_id - 1) * page_size))
		rows = pg_cursor.fetchall()
		pg_conn.close()

		# return result
		response = {'result' : True, 'notes' : []}
		for row in rows:
			response['notes'].append({
				'note_id' : str(row[0]),
				'usr_nick' : row[1],
				'pub_time' : str(row[2]),
				'title' : row[3],
				'tags' : row[4]
			})
		return response
