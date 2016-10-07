#!/usr/bin/python
# -*- coding:utf-8 -*-

# Author 		: 	Lv Yang
# Created 		: 	05 October 2016
# Modified 		: 	07 October 2016
# Version 		: 	1.0

"""
This file encapsulate several operations about interaction, includes :
a. increase(or decrease) one note's agree_num(or oppose_num or collect_num or comment_num)
b. get somebody's agree-and-oppose records towards one specific note
c. add a record of somebody agree-or-oppose one specific note
d. delete a record of somebody agree-or-oppose one specific note
e. judge whether somebody has collected one specific note
f. judge whether somebody has cared another user
"""

def affect_note(mongoconn,db_name,note_id,field,value):
    """
    increase(or decrease) one note's agree_num(or oppose_num or collect_num or comment_num)
    parameters :
        mongoconn is a MongoClient, you can get it from 'mongoconn_model.py'
        note_id is the note's _id
        field is 'agree_num' or 'oppose_num' or 'collect_num' or 'comment_num'
        value is 1 or -1
    """
    pass


def agree_oppose_record(mongoconn,db_name,user_id,note_id):
    """
    get somebody's agree-and-oppose records towards one specific note
    return :
        if exists, it return the action_type field ( action_type=0 or 1 )
        if not, it return None
    """
    pass


def agree_oppose_add(mongoconn,db_name,user_id,note_id,action_type):
    """
    add a record of somebody agree-or-oppose one specific note
    parameters :
        action_type = 0, agree
        action_type = 1, oppose
    """
    pass


def agree_oppose_delete(mongoconn,db_name,user_id,note_id,action_type):
    """
    delete a record of somebody agree-or-oppose one specific note
    """
    pass


def exist_collect(mongoconn,db_name,user_id,note_id):
    """
    judge whether somebody has collected one specific note
    return :
        True if yes, False if not
    """
    pass


def exist_care(mongoconn,db_name,carer_id,cared_id):
    """
    judge whether somebody has cared another user
    parameters :
        carer_id is your id
        cared_id is another user's id
    return :
        True if yes, False if not
    """
    pass
