#!/usr/bin/python
# -*- coding:utf-8 -*-

# Author 		: 	Lv Yang
# Created 		: 	25 September 2016
# Modified 		: 	25 September 2016
# Version 		: 	1.0

"""
This script is the entrance of the server program
"""

import sys
sys.path.append("../model")
sys.path.append("../handler")

import flask

import conf_model
import handler_factory


def help():
    """
    print help information of how to use this script
    """
    inform = "This script is the driver program of deepnote server\
        \r\n\r\nhow to run when debug :\
        \r\n\tpython main.py arg1 arg2\
        \r\nparameters :\
        \r\n\t'arg1' is the bind ip\
        \r\n\t'arg2' is the bind port\
        \r\nfor example :\
        \r\n\tpython main.py 0.0.0.0 8081\
        \r\n\r\nhow to run when deploy :\
        \r\n\tuwsgi --ini ../conf/uwsgi8081.ini"
    print inform


# read server configuration
Shared_Conf = conf_model.read("../conf/server.conf")


# create a server app
Server_App = flask.Flask(__name__)
Server_App.secret_key = '\r\x9d1\xd1\xccW\x9e\xa6\x9a\x97[\xb1=\x93\x87\x15s<\xe8\xe3\x13DL?'


# define the interface
@Server_App.route("/action",methods=['POST'])
def action():
    # get global conf
    global Shared_Conf

    # get Post_Data, Post_Files, Session
    post_data = flask.request.form
    post_files = flask.request.files
    usr_session = flask.session

    # deal with it
    response = {}
    try:
        action_id = post_data['action_id']
        handler = handler_factory.HandlerFactory.produce(action_id,post_data,post_files,usr_session,Shared_Conf)
        response = handler.perform()
    except Exception,e:
        print str(e)

    # return response to client
    return flask.jsonify(response)


if __name__ == '__main__':
    bind_ip = None
    bind_port = None
    try:
        bind_ip = sys.argv[1]
        bind_port = int(sys.argv[2])
    except Exception,e:
        print str(e)
        help()
        sys.exit(1)
    Server_App.run(host=bind_ip,port=bind_port)
