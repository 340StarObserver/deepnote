#!/usr/bin/python
# -*- coding:utf-8 -*-

# Author 		: 	Lv Yang
# Created 		: 	05 October 2016
# Modified 		: 	07 October 2016
# Version 		: 	1.0

"""
This file encapsulate several operations about note, includes :
a. insert a new note into mongo
b. insert a new note into elasticsearch
c. judge whether a note exists
d. modify a note in mongo
e. modify a note in elasticsearch
f. delete a note from mongo
g. delete a note from elasticsearch
"""

def add_note_to_mongo(mongoconn,db_name,title,own_id,own_nick,feel,labels,link,ref):
    """
    insert a new note into mongo
    
    parameters :
        mongoconn is a MongoClient, you can get it from 'mongoconn_model.py'

        title is the note's title
        feel is the note's feel
        link is the note's source_link
        ref is the note's source_ref
        own_id, own_nick is the owner's info, you can get it from session
    """
    pass


def add_note_to_es(esconn,index,type,note_id,title,feel,labels,ref):
    """
    insert a new note into elasticsearch
    parameters :
        esconn is a Elasticsearch object, you can get it from 'esconn_model.py'
    """
    pass


def exist_note(mongoconn,db_name,note_id):
    """
    judge whether a note in mongodb exists
    parameters :
        mongoconn is a MongoClient, you can get it from 'mongoconn_model.py'
        note_id is the note's _id
    return :
        if exists, it return this note's own_id
        if not, it return None
    """
    pass


def modify_note_in_mongo(mongoconn,db_name,note_id,feel,labels,link,ref):
    """
    modify a note in mongo
    """
    pass


def modify_note_in_es(esconn,index,type,note_id,feel,labels,ref):
    """
    modify a note in elasticsearch
    """
    pass


def delete_note_from_mongo(mongoconn,db_name,note_id):
    """
    delete a note from mongo
    """
    pass


def delete_note_from_es(esconn,index,type,note_id):
    """
    delete a note from elasticsearch
    """
    pass
