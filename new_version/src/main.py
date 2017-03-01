#!/usr/bin/python
# -*- coding:utf-8 -*-

# Author 		: 	Lv Yang
# Created 		: 	01 March 2017
# Modified 		: 	01 March 2017
# Version 		: 	1.0

import flask

import sys
sys.path.append("common")
sys.path.append("handlers")

from appconf import AppConf
from applogger import AppLogger

from handlerfactory import HandlerFactory


# create a server app
App = flask.Flask(__name__)
App.secret_key = '\r\x9d1\xd1\xccW\x9e\xa6\x9a\x97[\xb1=\x93\x87\x15s<\xe8\xe3\x13DL?'


# define the unified interface
@App.route("/action",methods=['POST'])
def action():
	# receive parameters
	post_data = flask.request.form
	post_files = flask.request.files
	usr_session = flask.session

	# deal
	response = {'result' : False}
	try:
		request_type = int(post_data['action_id'])
		handler = HandlerFactory.produce(request_type)(post_data, post_files, usr_session)
		response = handler.perform()
	except Exception, e:
		AppLogger.getInstance().error(str(e))

	# return
	return flask.jsonify(response)


if __name__ == '__main__':
	# 1. init conf
	AppConf.init("common/app.conf")

	# 2. init logger
	AppLogger.init(\
		AppConf.get('log', 'path'), \
		AppConf.get('log', 'max_mb'), \
		AppConf.get('log', 'backup_num')
	)

	# 3. init handler factory
	HandlerFactory.init()

	# 4. start run
	App.run(host = sys.argv[1], port = int(sys.argv[2]))
