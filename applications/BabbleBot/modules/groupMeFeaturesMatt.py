#!/usr/bin/env python
#-*- coding: utf-8 -*-
from gluon import *
import os
import json
import markovify
import types

def getCommonCurseWords(com, translator, userID = 'ALL'):
    curseWords = {'fuck': [0,{}], 'piss': [0,{}], 'shit' : [0,{}], 'damn' : [0,{}], 'ass' : [0,{}], 'dick' : [0,{}], 'bastard' : [0,{}], 'prick' : [0,{}], 'motherfucker' : [0,{}], 'gosh-golly' : [0,{}]}
    userDict = {}

    for k,val in com.iteritems():
        try:
            v = json.loads(val)
            msg = str(v['text']).lower() # make lower
            msg = msg.strip(',').strip('.').strip('!').strip('"').strip('\'').strip('`') # rid of annoying stuff
            l = msg.split(' ')
            for curse,data in curseWords.iteritems():
                if curse in l:
                    if userID == 'ALL' and len(v['sender_id']) > 6 and v['sender_id'] != 'system' and v['sender_id'] != 'calendar':
                        curseWords[curse][0] += 1
                        if not v['sender_id'] in curseWords[curse][1]:
                            curseWords[curse][1][v['sender_id']] = 0
                        curseWords[curse][1][v['sender_id']] += 1
                    # for users
                    elif userID == v['sender_id'] and len(v['sender_id']) > 6 and v['sender_id'] != 'system' and v['sender_id'] != 'calendar':
                        curseWords[curse][0] += 1
        except:
            # IF EMOJIES
            pass

    finalDict = {}
    if userID != 'ALL':
        return curseWords

    for k, val in curseWords.iteritems():
        if val[0] != 0:
            userDict = val[1]
            namedDict = {}
            for user, num in userDict.iteritems():
                if user in translator and translator[user] != 'GroupMe' and user != 'calendar' and user != 'system':
                    if userID == 'ALL' or user == userID:
                        namedDict[translator[user]] = num

            finalList = []
            finalList.append(val[0])
            finalList.append(namedDict)
            finalDict[k] = finalList
    
    return finalDict
