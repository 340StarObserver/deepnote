#!/usr/bin/python
# -*- coding:utf-8 -*-

# Author 		: 	Lv Yang
# Created 		: 	05 October 2016
# Modified 		: 	07 October 2016
# Version 		: 	1.0

"""
This file encapsulate several operations about searching, includes :
a. search from elasticsearch by giving a sentence
b. get a note's base info from mongodb
c. get a note's detail info from mongodb
"""

def fuzzySearch(esconn,index,type,sentence,page_id,page_size):
    """
    search from elasticsearch by giving a sentence

    parameters :
        esconn is a Elasticsearch object, you can get it from 'esconn_model.py'
        index is the index name of elasticsearch
        type is the type name of elasticsearch

        sentence is a sentence that user input
        page_id is the id of current page
        page_size is the size of current page

    return :
        a list like [ note_id1, note_id2, note_id3 ]
    """
    pass


def note_baseinfo(mongoconn,db_name,note_id):
    """
    get a note's base info from mongodb

    parameters :
        mongoconn is a MongoClient, you can get it from 'mongoconn_model.py'
        note_id is the note's _id

    return :
        if exists, it return a dict like {'_id':'xx','title':'yy','own_id':'aa','own_nick':'bb','pub_time':cc,'feel':'dd','labels':'ee'}
        if not, it return None
    """
    pass


def note_detailinfo(mongoconn,db_name,note_id):
    """
    get a note's detail info from mongodb
    return :
        if exists, a dict like
            {'_id':'xx','title':'yy','own_id':'aa','own_nick':'bb',
            'pub_time':cc,'feel':'dd','labels':'ee',
            'source_link':'ff','source_ref':'gg',
            'agree_num':3,'oppose_num':4,'collect_num':5,'comment_num':6}
        if not, it return None
    """
    pass
