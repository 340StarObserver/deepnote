#!/usr/bin/python
# -*- coding:utf-8 -*-

# Author 		: 	Lv Yang
# Created 		: 	01 March 2017
# Modified 		: 	01 March 2017
# Version 		: 	1.0

import logging
from logging.handlers import RotatingFileHandler

class AppLogger(object):

	@staticmethod
	def init(log_file, max_MB, backup_num):
		handler = RotatingFileHandler(filename = log_file,\
			mode = 'a',\
			maxBytes = max_MB * 1024 * 1024,\
			backupCount = backup_num)
		handler.setFormatter(\
			logging.Formatter(\
				'%(asctime)s [%(filename)s][l:%(lineno)d][p:%(process)d][t:%(thread)d] %(levelname)s %(message)s'
			)
		)
		logger = logging.getLogger()
		logger.setLevel(logging.DEBUG)
		logger.addHandler(handler)
		AppLogger._logger = logger

	@staticmethod
	def getInstance():
		return AppLogger._logger
