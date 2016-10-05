#!/usr/bin/python
# -*- coding:utf-8 -*-

# Author 		: 	Lv Yang
# Created 		: 	05 October 2016
# Modified 		: 	05 October 2016
# Version 		: 	1.0

"""
This file encapsulate several operations about note, includes :
a. insert a new note into mongo and elasticsearch
b. judge whether a note exists
c. modify a note in mongo and elasticsearch
d. delete a note from mongo and elasticsearch
"""

def add_note(mongoconn,title,own_id,own_nick,feel,labels,link,ref,es_host,es_port,es_index,es_type):
    """
    insert a new note into mongo and elasticsearch
    
    parameters :
        mongoconn is a MongoClient, you can get it from 'mongoconn_model.py'

        title is the note's title
        feel is the note's feel
        link is the note's source_link
        ref is the note's source_ref
        own_id, own_nick is the owner's info, you can get it from session

        es_host,es_port,es_index,es_type is elasticsearch's info, you can get it from global server conf
    """
    pass


def exist_note(mongoconn,note_id):
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


def modify_note(mongoconn,note_id,feel,labels,link,ref,es_host,es_port,es_index,es_type):
    """
    modify a note in mongo and elasticsearch
    """
    pass


def delete_note(mongoconn,note_id,es_host,es_port,es_index,es_type):
    """
    delete a note from mongo and elasticsearch
    """
    pass
