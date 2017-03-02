#!/usr/bin/python
# -*- coding:utf-8 -*-

# Author 		: 	Lv Yang
# Created 		: 	01 March 2017
# Modified 		: 	01 March 2017
# Version 		: 	1.0

from basehandler import BaseHandler
from smshandler import SmsHandler
from registhandler import RegistHandler


""" factory of all handlers """
class HandlerFactory(object):
	
	@staticmethod
	def init():
		HandlerFactory.factory = {
			101 : SmsHandler,
			102 : RegistHandler
		}

	@ staticmethod
	def produce(request_type):
		try:
			return HandlerFactory.factory[request_type]
		except:
			return BaseHandler
