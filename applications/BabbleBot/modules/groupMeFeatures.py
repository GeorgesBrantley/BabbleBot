#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gluon import *
import json

def getLikesPerUser(com, translator):
    userDict = {}
    for k,val in com.iteritems():
        try:
            v = json.loads(val)
            if v['sender_id'] in userDict:
                userDict[v['sender_id']] += int(len(v['favorited_by']))
            else:
                userDict[v['sender_id']] = len(v['favorited_by'])
        except:
            pass
    namedDict = {}
    print translator
    for k, val in userDict.iteritems():
        if k in translator:
            namedDict[translator[k]] = val

    return namedDict
