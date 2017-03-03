#!/usr/bin/python
# -*- coding:utf-8 -*-

# Author 		: 	Lv Yang
# Created 		: 	03 March 2017
# Modified 		: 	03 March 2017
# Version 		: 	1.0

from basehandler import BaseHandler

class LogoutHandler(BaseHandler):

	def __init__(self, post_data, post_files, usr_session):
		super(LogoutHandler, self).__init__(post_data, post_files, usr_session)

	def perform(self):
		self._usr_session.clear()
		return {'result' : True}
