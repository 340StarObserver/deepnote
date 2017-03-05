#!/usr/bin/python
# -*- coding:utf-8 -*-

# Author 		: 	Lv Yang
# Created 		: 	05 March 2017
# Modified 		: 	05 March 2017
# Version 		: 	1.0

import base64
import random

import sys
sys.path.append("../common")

from appconf import AppConf
from appvalid import AppValid
from applogger import AppLogger
from ossconn import OssConn

from basehandler import BaseHandler


""" set a user's head """
class HeadHandler(BaseHandler):

	def __init__(self, post_data, post_files, usr_session):
		super(HeadHandler, self).__init__(post_data, post_files, usr_session)

	def perform(self):
		# if not login
		if 'usr_id' not in self._usr_session:
			return {'result' : False, 'reason' : 1}

		# if token is wrong
		token = int(self._post_data['token'])
		if 'token' not in self._usr_session or token != self._usr_session['token']:
			return {'result' : False, 'reason' : 2}

		# analyze head image
		try:
			head = base64.b64decode(self._post_data['head'])
			w = True
		except Exception, e:
			w = False
			AppLogger.getInstance().error(str(e))
		if w is False:
			return {'result' : False, 'reason' : 3}

		# try to save head image
		try:
			# conn to oss and push
			oss_conn = OssConn(AppConf.get('oss', 'access_id'), \
				AppConf.get('oss', 'access_key'), \
				AppConf.get('oss', 'end_point'), \
				AppConf.get('oss', 'bucket'))
			key = "%s/%d.png" % (AppConf.get('oss', 'head_dir'), self._usr_session['usr_id'])
			res = oss_conn.push(key, head)

			# write log
			msg = "[usr:%d][act:107][res:%s]" % (self._usr_session['usr_id'], str(res))
			AppLogger.getInstance().info(msg)
		except Exception, e:
			w = False
			AppLogger.getInstance().error(str(e))
		if w is False:
			return {'result' : False, 'reason' : 4}

		# create a new token for next use
		token = random.randint(AppConf.get('auth', 'token_min'), AppConf.get('auth', 'token_max'))
		self._usr_session['token'] = token

		# return result
		return {'result' : True, 'token' : token}
