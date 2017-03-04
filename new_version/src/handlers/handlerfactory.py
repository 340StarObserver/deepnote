#!/usr/bin/python
# -*- coding:utf-8 -*-

# Author 		: 	Lv Yang
# Created 		: 	01 March 2017
# Modified 		: 	03 March 2017
# Version 		: 	1.0

from basehandler import BaseHandler
from smshandler import SmsHandler
from registhandler import RegistHandler
from loginhandler import LoginHandler
from logouthandler import LogoutHandler
from usrinfohandler import UsrinfoHandler
from signaturehandler import SignatureHandler


""" factory of all handlers """
class HandlerFactory(object):
	
	@staticmethod
	def init():
		HandlerFactory.factory = {
			101 : SmsHandler,
			102 : RegistHandler,
			103 : LoginHandler,
			104 : LogoutHandler,
			105 : UsrinfoHandler,
			106 : SignatureHandler
		}

	@ staticmethod
	def produce(request_type):
		try:
			return HandlerFactory.factory[request_type]
		except:
			return BaseHandler
