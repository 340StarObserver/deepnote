#!/usr/bin/python
# -*- coding:utf-8 -*-

# Author 		: 	Lv Yang
# Created 		: 	05 October 2016
# Modified 		: 	05 October 2016
# Version 		: 	1.0

"""
This file encapsulate several operations about user's account, includes :
a. judge whether an account exists
b. get one account's info
c. set one account's password
d. upload head image to OSS
"""

def exist_account(mongoconn,phone):
    """
    judge whether an account exists
    parameters :
        mongoconn is a MongoClient, you can get it from 'mongoconn_model.py'
        phone is the account's username, like '13912341234'
    return :
        True if exists, False if not
    """
    pass


def account_info(mongoconn,phone):
    """
    get one account's info
    return :
        a dict if exists, for example : {'_id':'13912341234','password':'xxx','nick':'yyy','signup_time':zzz,'signature':'aaa'}
        None if not
    """
    pass


def set_pwd(mongoconn,pwd):
    """
    set one account's password
    """
    pass


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
    pass
