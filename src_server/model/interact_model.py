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

from bson import ObjectId


def affect_note(mongoconn,db_name,note_id,field,value):
    """
    increase(or decrease) one note's agree_num(or oppose_num or collect_num or comment_num)
    parameters :
        mongoconn is a MongoClient, you can get it from 'mongoconn_model.py'
        note_id is the note's _id
        field is 'agree_num' or 'oppose_num' or 'collect_num' or 'comment_num'
        value is 1 or -1
    """
    factor_1 = {'_id':ObjectId(note_id)}
    factor_2 = {'$inc':{field:value}}
    mongoconn[db_name]['note_extra'].update_one(factor_1,factor_2)


def agree_oppose_record(mongoconn,db_name,user_id,note_id):
    """
    get somebody's agree-and-oppose records towards one specific note
    return :
        if exists, it return the action_type field ( action_type=0 or 1 )
        if not, it return None
    """
    factor_1 = {'user_id':user_id,'note_id':note_id,'action_type':{'$lt':2}}
    factor_2 = {'_id':0,'action_type':1}
    res = mongoconn[db_name]['note_action'].find_one(factor_1,factor_2)
    if res is not None:
        return int(res['action_type'])
    return None


def agree_oppose_add(mongoconn,db_name,user_id,note_id,action_type):
    """
    add a record of somebody agree-or-oppose one specific note
    parameters :
        action_type = 0, agree
        action_type = 1, oppose
    """
    doc = {}
    doc['user_id'] = user_id
    doc['note_id'] = note_id
    doc['action_type'] = action_type
    mongoconn[db_name]['note_action'].insert_one(doc)


def agree_oppose_delete(mongoconn,db_name,user_id,note_id,action_type):
    """
    delete a record of somebody agree-or-oppose one specific note
    """
    factor = {'user_id':user_id,'note_id':note_id,'action_type':action_type}
    mongoconn[db_name]['note_action'].delete_one(factor)


def exist_collect(mongoconn,db_name,user_id,note_id):
    """
    judge whether somebody has collected one specific note
    return :
        True if yes, False if not
    """
    factor = {'user_id':user_id,'note_id':note_id}
    res = mongoconn[db_name]['note_collect'].find_one(factor)
    return res != None


def exist_care(mongoconn,db_name,carer_id,cared_id):
    """
    judge whether somebody has cared another user
    parameters :
        carer_id is your id
        cared_id is another user's id
    return :
        True if yes, False if not
    """
    factor = {'carer_id':carer_id,'cared_id':cared_id}
    res = mongoconn[db_name]['care_record'].find_one(factor)
    return res != None
