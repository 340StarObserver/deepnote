#!/usr/bin/python
# -*- coding:utf-8 -*-

# Author 		: 	Lv Yang
# Created 		: 	27 February 2017
# Modified 		: 	27 February 2017
# Version 		: 	1.0

import oss2

""" OSS connection manager """
class OssConn(object):
	
	def __init__(self, access_id, access_key, end_point, bucket):
		auth = oss2.Auth(access_id, access_key)
		self._conn = oss2.Bucket(auth, end_point, bucket)

	def push(self, key_str, data_bin):
		res = self._conn.put_object(key_str, data_bin)
		return (res.status, res.request_id, res.etag)
