#!/usr/bin/python
# -*- coding:utf-8 -*-

# Author 		: 	Lv Yang
# Created 		: 	05 October 2016
# Modified 		: 	07 October 2016
# Version 		: 	1.0

"""
This file encapsulate several operations about user's account, includes :
a. judge whether an account exists
b. get one account's info
c. set one account's password
d. upload head image to OSS
"""

import oss2

def exist_account(mongoconn,db_name,phone):
    """
    judge whether an account exists
    parameters :
        mongoconn is a MongoClient, you can get it from 'mongoconn_model.py'
        phone is the account's username, like '13912341234'
    return :
        True if exists, False if not
    """
    record = mongoconn[db_name]['user_info'].find_one({'_id':phone})
    return record != None


def account_info(mongoconn,db_name,phone):
    """
    get one account's info
    return :
        a dict if exists, for example : {'_id':'13912341234','password':'xxx','nick':'yyy','signup_time':zzz,'signature':'aaa'}
        None if not
    """
    return mongoconn[db_name]['user_info'].find_one({'_id':phone})


def set_pwd(mongoconn,db_name,phone,pwd):
    """
    set one account's password
    """
    factor1 = {'_id':phone}
    factor2 = {'$set':{'password':pwd}}
    mongoconn[db_name]['user_info'].update_one(factor1,factor2)


def upload_head(access_id,access_key,end_point,bucket_name,head_dir,username,image_data):
    """
    upload head image to OSS
    parameters :
        access_id, access_key is for auth
        end_point is an url, you can get it from the global server config
        bucket_name is the name of your oss bucket
        head_dir is the name of the directory which stores head images
        username is the user's phone
        image_data is an image's binary data
    """
    auth = oss2.Auth(access_id,access_key)
    bucket_conn = oss2.Bucket(auth,end_point,bucket_name)
    path = "%s/%s.jpg"%(head_dir,username)
    result = bucket_conn.put_object(path,image_data)
    return (result.status,result.request_id,result.etag)
