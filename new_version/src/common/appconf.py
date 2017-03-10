#!/usr/bin/python
# -*- coding:utf-8 -*-

# Author 		: 	Lv Yang
# Created 		: 	15 February 2017
# Modified 		: 	08 March 2017
# Version 		: 	1.0

import ConfigParser
import sys

""" Application's configure reader """
class AppConf(object):

	@staticmethod
	def init(filename):
		res = {'log' : {}, 'pg' : {}, 'oss' : {}, 'sms' : {}, 'auth' : {}}
		config = ConfigParser.ConfigParser()
		try:
			reload(sys)
			sys.setdefaultencoding('utf8')
			config.read(filename)

			# log
			res['log']['path'] = config.get('log', 'path')
			res['log']['max_mb'] = int(config.get('log', 'max_mb'))
			res['log']['backup_num'] = int(config.get('log', 'backup_num'))

			# postgresql
			res['pg']['host'] = config.get('pg', 'host')
			res['pg']['port'] = int(config.get('pg', 'port'))
			res['pg']['r_usr'] = config.get('pg', 'r_usr')
			res['pg']['r_pwd'] = config.get('pg', 'r_pwd')
			res['pg']['w_usr'] = config.get('pg', 'w_usr')
			res['pg']['w_pwd'] = config.get('pg', 'w_pwd')
			res['pg']['rw_usr'] = config.get('pg', 'rw_usr')
			res['pg']['rw_pwd'] = config.get('pg', 'rw_pwd')

			# oss
			res['oss']['access_id'] = config.get('oss', 'access_id')
			res['oss']['access_key'] = config.get('oss', 'access_key')
			res['oss']['end_point'] = config.get('oss', 'end_point')
			res['oss']['bucket'] = config.get('oss', 'bucket')
			res['oss']['head_dir'] = config.get('oss', 'head_dir')

			# sms
			res['sms']['access_key'] = int(config.get('sms', 'access_key'))
			res['sms']['secret_key'] = config.get('sms', 'secret_key')
			res['sms']['code_min'] = int(config.get('sms', 'code_min'))
			res['sms']['code_max'] = int(config.get('sms', 'code_max'))
			res['sms']['url'] = config.get('sms', 'url')
			res['sms']['time_limit'] = int(config.get('sms', 'time_limit'))

			# auth
			res['auth']['token_min'] = int(config.get('auth', 'token_min'))
			res['auth']['token_max'] = int(config.get('auth', 'token_max'))

			AppConf._conf = res
		except Exception, e:
			print "fail to read configuration from %s" % (filename)
			print str(e)
			sys.exit(1)

	@staticmethod
	def get(para1, para2):
		return AppConf._conf[para1][para2]

if __name__ == '__main__':
	AppConf.init("app.conf")
	print AppConf._conf
