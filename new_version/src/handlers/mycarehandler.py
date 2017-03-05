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

from basehandler import BaseHandler


""" get users' info who I care """
class MycareHandler(BaseHandler):

	def __init__(self, post_data, post_files, usr_session):
		super(MycareHandler, self).__init__(post_data, post_files, usr_session)

	def perform(self):
		# if parameters invalid or not login
		page_id = int(self._post_data['page_id'])
		page_size = int(self._post_data['page_size'])
		if page_id <= 0 or page_size <= 0 or 'usr_id' not in self._usr_session:
			return {'result' : False}

		# conn to pg
		pg_conn = psycopg2.connect(\
			host = AppConf.get('pg_r', 'host'), \
			port = AppConf.get('pg_r', 'port'), \
			user = AppConf.get('pg_r', 'usr'), \
			password = AppConf.get('pg_r', 'pwd'), \
			database = "dp_note")
		pg_cursor = pg_conn.cursor()

		# do query
		offset = (page_id - 1) * page_size
		pg_cursor.execute(\
			"select userinfo.usr_nick, userinfo.regist_time, userinfo.signature \
				from usercare, userinfo \
				where usercare.usr_id=%s and usercare.care_nick=userinfo.usr_nick \
				order by usercare.care_time desc limit %s offset %s",\
			(self._usr_session['usr_id'], page_size, offset))
		rows = pg_cursor.fetchall()
		pg_conn.close()

		# return result
		response = {'result' : True, 'cares' : []}
		for row in rows:
			response['cares'].append({
				'usr_nick' : row[0],
				'regist_time' : str(row[1]),
				'signature' : row[2]
			})
		return response
