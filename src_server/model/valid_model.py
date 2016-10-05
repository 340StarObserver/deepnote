#!/usr/bin/python
# -*- coding:utf-8 -*-

# Author 		: 	Lv Yang
# Created 		: 	25 September 2016
# Modified 		: 	05 October 2016
# Version 		: 	1.0

"""
This script used to judge whether data is valid, includes :
1. mobile phone number
2. password
3. ...( wait for others )
"""

import re

def is_valid_phone(phone):
    """
    judge whether a phone number is valid
    """
    pattern = re.compile('^(13[0-9]|14[5|7]|15[0|1|2|3|5|6|7|8|9]|18[0|1|2|3|5|6|7|8|9])\\d{8}$')
    return pattern.match(phone)!=None

def is_valid_pwd(pwd):
    """
    judge whether a password is valid
    """
    pattern = re.compile('^[0-9a-f]{32}$')
    return pattern.match(pwd)!=None

def is_valid_nick(nick):
    """
    judge whether a nick is valid
    """
    return len(nick) > 0

def is_valid_notetitle(title):
    """
    judge whether a note's title is valid
    """
    return len(title) > 0

def is_valid_notefeel(feel):
    """
    judge whether a note's feel is valid
    """
    return len(feel) > 0
