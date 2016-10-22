#!/usr/bin/python
# -*- coding:utf-8 -*-

# Author 		: 	Lv Yang
# Created 		: 	05 October 2016
# Modified 		: 	22 October 2016
# Version 		: 	1.0

"""
This file encapsulate several operations about searching, includes :
a. search from elasticsearch by giving a sentence
b. get a note's base info from mongodb
c. get a note's detail info from mongodb
"""

from bson import ObjectId
import json


def fuzzySearch(esconn,index,doc_type,sentence,page_id,page_size):
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
    # prepare query body
    body = {}
    body['size'] = 10 * page_size
    body['_source'] = ['nosource']
    body['sort'] = [{'_score':{'order':'desc'}}]
    body['query'] = {'filtered':{'query':{'bool':{'should':[]}}}}
    body['query']['filtered']['query']['bool']['should'].append({'match':{'title':{'query':sentence,'boost':20}}})
    body['query']['filtered']['query']['bool']['should'].append({'match':{'source_ref':{'query':sentence,'boost':1}}})
    body['query']['filtered']['query']['bool']['should'].append({'match':{'feel':{'query':sentence,'boost':2}}})
    body['query']['filtered']['query']['bool']['should'].append({'match':{'labels':{'query':sentence,'boost':5}}})
    # do query
    res = esconn.search(index=index,doc_type=doc_type,body=body)
    res = res['hits']['hits']
    # select notes in this page
    note_ids = []
    n = len(res)
    start_i = min((page_id-1)*page_size,n)
    over_i = min(page_id*page_size,n)
    while start_i < over_i:
        note_ids.append(res[start_i]['_id'])
        start_i+=1
    return note_ids


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
    res = mongoconn[db_name]['note_base'].find_one({'_id':ObjectId(note_id)})
    if res is not None:
        res['_id'] = str(res['_id'])
    return res


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
    factor = {'_id':ObjectId(note_id)}
    res_base = mongoconn[db_name]['note_base'].find_one(factor)
    res_extra = mongoconn[db_name]['note_extra'].find_one(factor)
    if res_base is not None and res_extra is not None:
        res = dict(res_base,**res_extra)
        res['_id'] = str(res['_id'])
        return res
    return None
