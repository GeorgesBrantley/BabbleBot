#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gluon import *
import json

def countCommentsPerUser(comments):
    user = {}
    for k,val in comments.iteritems():
        try:
            v = json.loads(val)
            if v['sender_id'] in user:
                user[v['sender_id']] += 1
            else:
                user[v['sender_id']] = 1
        except:
            pass
    return user

def getPastName(comments):
    pastNames = []
    for k,val in comments.iteritems():
        try:
            v = json.loads(val)
            if v['sender_id'] == 'system':
                if 'changed name to' in v['text'].encode("utf-8"):
                     pastNames.append(v['text'].encode("utf-8"))
        except:
            pass
    return pastNames

def getNumKicked(comments):
    numKicked = []
    for k,val in comments.iteritems():
        try:
            v = json.loads(val)
            if v['sender_id'] == 'system':
                if 'removed' in v['text'].encode("utf-8"):
                     numKicked.append(v['text'].encode("utf-8"))
        except:
            pass
    return numKicked
