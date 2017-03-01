#!/usr/bin/python
# -*- coding:utf-8 -*-

# Author 		: 	Lv Yang
# Created 		: 	01 March 2017
# Modified 		: 	01 March 2017
# Version 		: 	1.0

""" base handler """
class BaseHandler(object):

	def __init__(self, post_data, post_files, usr_session):
		self._post_data = post_data
		self._post_files = post_files
		self._usr_session = usr_session
		
	def perform(self):
		return {'result' : False}
