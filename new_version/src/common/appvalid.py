#!/usr/bin/python
# -*- coding:utf-8 -*-

# Author 		: 	Lv Yang
# Created 		: 	01 March 2017
# Modified 		: 	17 March 2017
# Version 		: 	1.0

import re

""" used to judge whether data is valid """
class AppValid(object):

	@staticmethod
	def validPhone(phone):
		pattern = re.compile('^(13[0-9]|14[5|7]|15[0|1|2|3|5|6|7|8|9]|18[0|1|2|3|5|6|7|8|9])\\d{8}$')
		return pattern.match(phone) != None

	@staticmethod
	def validPasswd(pwd):
		pattern = re.compile('^[0-9a-f]{32}$')
		return pattern.match(pwd) != None

	@staticmethod
	def validNick(nick):
		return len(nick) <= 32

	@staticmethod
	def validSignature(signature):
		return len(signature) <= 128

	@staticmethod
	def validNoteTitle(title):
		n = len(title)
		if n > 0 and n <= 128:
			return True
		return False

	@staticmethod
	def validNoteFeel(feel):
		return len(feel) > 0
