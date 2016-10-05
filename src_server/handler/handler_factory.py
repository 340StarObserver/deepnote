#!/usr/bin/python
# -*- coding:utf-8 -*-

# Author 		: 	Lv Yang
# Created 		: 	24 September 2016
# Modified 		: 	05 October 2016
# Version 		: 	1.0

"""
This script defines a factory which produces different kinds of handlers
"""

from base_handler import BaseHandler
from verifycode_handler import VerifycodeHandler
from regist_handler import RegistHandler
from login_handler import LoginHandler
from logout_handler import LogoutHandler
from userinfo_handler import UserinfoHandler
from setsignature_handler import SetsignatureHandler
from sethead_handler import SetheadHandler
from setpwd_handler import SetpwdHandler
from forgetpwd_handler import ForgetpwdHandler
from addnote_handler import AddnoteHandler
from getnotebyuser_handler import GetnotebyuserHandler
from modifynote_handler import ModifynoteHandler
from rmnote_handler import RmnoteHandler
from syncnote_handler import SyncnoteHandler
from getnotebytime_handler import GetnotebytimeHandler
from searchnote_handler import SearchnoteHandler
from notedetail_handler import NotedetailHandler
from getcomment_handler import GetcommentHandler
from agree_handler import AgreeHandler
from oppose_handler import OpposeHandler
from collect_handler import CollectHandler
from getcollect_handler import GetcollectHandler
from writecomment_handler import WritecommentHandler
from message_handler import MessageHandler
from care_handler import CareHandler
from getcare_handler import GetcareHandler

class HandlerFactory :
    @staticmethod
    def produce(action_id,post_data,post_files,usr_session,server_conf):
        """
        produce a corresponding handler based on the action_id
        parameters :
            'post_data' is the POST data which not files
            'post_files' is the POST files
            'usr_session' is session of the current user
            'server_conf' is the global shared config
        """
        try:
            action_id = int(action_id)
        except:
            action_id = 0
        if action_id is 101:
            return VerifycodeHandler(post_data,post_files,usr_session,server_conf)
        if action_id is 102:
            return RegistHandler(post_data,post_files,usr_session,server_conf)
        if action_id is 103:
            return LoginHandler(post_data,post_files,usr_session,server_conf)
        if action_id is 104:
            return LogoutHandler(post_data,post_files,usr_session,server_conf)
        if action_id is 105:
            return UserinfoHandler(post_data,post_files,usr_session,server_conf)
        if action_id is 106:
            return SetsignatureHandler(post_data,post_files,usr_session,server_conf)
        if action_id is 107:
            return SetheadHandler(post_data,post_files,usr_session,server_conf)
        if action_id is 108:
            return SetpwdHandler(post_data,post_files,usr_session,server_conf)
        if action_id is 109:
            return ForgetpwdHandler(post_data,post_files,usr_session,server_conf)
        if action_id is 201:
            return AddnoteHandler(post_data,post_files,usr_session,server_conf)
        if action_id is 202:
            return GetnotebyuserHandler(post_data,post_files,usr_session,server_conf)
        if action_id is 203:
            return ModifynoteHandler(post_data,post_files,usr_session,server_conf)
        if action_id is 204:
            return RmnoteHandler(post_data,post_files,usr_session,server_conf)
        if action_id is 205:
            return SyncnoteHandler(post_data,post_files,usr_session,server_conf)
        if action_id is 301:
            return GetnotebytimeHandler(post_data,post_files,usr_session,server_conf)
        if action_id is 302:
            return SearchnoteHandler(post_data,post_files,usr_session,server_conf)
        if action_id is 303:
            return NotedetailHandler(post_data,post_files,usr_session,server_conf)
        if action_id is 304:
            return GetcommentHandler(post_data,post_files,usr_session,server_conf)
        if action_id is 401:
            return AgreeHandler(post_data,post_files,usr_session,server_conf)
        if action_id is 402:
            return OpposeHandler(post_data,post_files,usr_session,server_conf)
        if action_id is 403:
            return CollectHandler(post_data,post_files,usr_session,server_conf)
        if action_id is 404:
            return GetcollectHandler(post_data,post_files,usr_session,server_conf)
        if action_id is 405:
            return WritecommentHandler(post_data,post_files,usr_session,server_conf)
        if action_id is 406:
            return MessageHandler(post_data,post_files,usr_session,server_conf)
        if action_id is 501:
            return CareHandler(post_data,post_files,usr_session,server_conf)
        if action_id is 502:
            return GetcareHandler(post_data,post_files,usr_session,server_conf)
        return BaseHandler(post_data,post_files,usr_session,server_conf)
