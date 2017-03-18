#!/usr/bin/python
# -*- coding:utf-8 -*-

# Author 		: 	Lv Yang
# Created 		: 	01 March 2017
# Modified 		: 	05 March 2017
# Version 		: 	1.0

from basehandler import BaseHandler

from smshandler import SmsHandler

from registhandler import RegistHandler
from loginhandler import LoginHandler
from logouthandler import LogoutHandler

from usrinfohandler import UsrinfoHandler
from signaturehandler import SignatureHandler
from headhandler import HeadHandler
from setpwdhandler import SetpwdHandler
from forgetpwdhandler import ForgetpwdHandler

from carehandler import CareHandler
from uncarehandler import UncareHandler
from mycarehandler import MycareHandler

from addnotehandler import AddnoteHandler
from notelisthandler import NotelistHandler


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
			106 : SignatureHandler,
			107 : HeadHandler,
			108 : SetpwdHandler,
			109 : ForgetpwdHandler,
			110 : CareHandler,
			111 : UncareHandler,
			112 : MycareHandler,
			201 : AddnoteHandler,
			202 : NotelistHandler
		}

	@ staticmethod
	def produce(request_type):
		try:
			return HandlerFactory.factory[request_type]
		except:
			return BaseHandler
