#!/usr/bin/python
# -*- coding:utf-8 -*-

# Author 		: 	Lv Yang
# Created 		: 	05 October 2016
# Modified 		: 	09 October 2016
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

import time
from bson import ObjectId


def add_note_to_mongo(mongoconn,db_name,title,own_id,own_nick,feel,labels,link,ref):
    """
    insert a new note into mongo
    
    parameters :
        mongoconn is a MongoClient, you can get it from 'mongoconn_model.py'

        title is the note's title
        feel is the note's feel
        labels is several labels like 'a,b,c'
        link is the note's source_link
        ref is the note's source_ref
        own_id, own_nick is the owner's info, you can get it from session

    return :
        the string format of this document's '_id'
    """
    # 1. insert into collection 'note_base'
    base_doc = {}
    base_doc['title'] = title
    base_doc['own_id'] = own_id
    base_doc['own_nick'] = own_nick
    base_doc['pub_time'] = int(time.time())
    base_doc['feel'] = feel
    base_doc['labels'] = labels
    mongoconn[db_name]['note_base'].insert_one(base_doc)
    doc_id = base_doc['_id']
    # 2, insert into collection 'note_extra'
    extra_doc = {}
    extra_doc['_id'] = doc_id
    extra_doc['source_link'] = link
    extra_doc['source_ref'] = ref
    extra_doc['agree_num'] = 0
    extra_doc['oppose_num'] = 0
    extra_doc['collect_num'] = 0
    extra_doc['comment_num'] = 0
    mongoconn[db_name]['note_extra'].insert_one(extra_doc)
    # 3. return doc's id
    return str(doc_id)


def add_note_to_es(esconn,index,doc_type,note_id,title,feel,labels,ref):
    """
    insert a new note into elasticsearch
    parameters :
        esconn is a Elasticsearch object, you can get it from 'esconn_model.py'
    """
    doc = {}
    doc['title'] = title
    doc['source_ref'] = ref
    doc['feel'] = feel
    doc['labels'] = labels
    esconn.create(index=index,doc_type=doc_type,body=doc,id=note_id)


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
    res = mongoconn[db_name]['note_base'].find_one({'_id':ObjectId(note_id)},{'_id':0,'own_id':1})
    if res is not None:
        return res['own_id']
    return None


def modify_note_in_mongo(mongoconn,db_name,note_id,feel,labels,link,ref):
    """
    modify a note in mongo
    """
    factor_1 = {'_id':ObjectId(note_id)}
    factor_2 = {'$set':{'feel':feel,'labels':labels,'pub_time':int(time.time())}}
    factor_3 = {'$set':{'source_link':link,'source_ref':ref}}
    mongoconn[db_name]['note_base'].update_one(factor_1,factor_2)
    mongoconn[db_name]['note_extra'].update_one(factor_1,factor_3)


def modify_note_in_es(esconn,index,doc_type,note_id,feel,labels,ref):
    """
    modify a note in elasticsearch
    """
    doc = {'doc':{}}
    doc['doc']['source_ref'] = ref
    doc['doc']['feel'] = feel
    doc['doc']['labels'] = labels
    esconn.update(index=index,doc_type=doc_type,id=note_id,body=doc)


def delete_note_from_mongo(mongoconn,db_name,note_id):
    """
    delete a note from mongo
    """
    factor = {'_id':ObjectId(note_id)}
    mongoconn[db_name]['note_base'].delete_one(factor)
    mongoconn[db_name]['note_extra'].delete_one(factor)


def delete_note_from_es(esconn,index,doc_type,note_id):
    """
    delete a note from elasticsearch
    """
    esconn.delete(index=index,doc_type=doc_type,id=note_id)
