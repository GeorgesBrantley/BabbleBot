#!/usr/bin/env python
#-*- coding: utf-8 -*-
from gluon import *
import os
import json
import markovify
import types

def getBestFriends(com, translator):
    backTranslate = {}
    for user in translator:
        backTranslate[translator[user]] = user
    print translator
    print backTranslate
    
    # Set up Dictionary : userScore = {'user' : {}, ...}
    userScore = {}
    for user in translator:
        if user != 'calendar' and user != 'system':
            userScore[user] = {}
            for subUser in translator:
                if user != subUser and subUser != 'calendar' and subUser != 'system':
                    userScore[user][subUser] = 0
      
    # For each commment
    for k,val in com.iteritems():
        try:
            v = json.loads(val)

            #Increment score for likes given and recieved
            user = str(v['sender_id'])
            if user != 'calendar' and user != 'system':
                for subUser in v['favorited_by']:
                    userScore[user][subUser] += 1
                    userScore[subUser][user] += 1
                    
            #Increment score for @'s
            msg = str(v['text'])
            if '@' in msg:
                try:
                    userName = msg.split("@")[1].split(" ")[0]
                    if userName in backTranslate:
                        userScore[user][backTranslate[userName]] += 3
                    if userName2 in backTranslate:
                        userScore[user][backTranslate[userName2]] += 3
                    userName3 = userName2 + ' ' + msg.split("@")[2].split(" ")[2]
                    if userName3 in backTranslate:
                        userScore[user][backTranslate[userName3]] += 3
                except:
                    print 'error'
                    pass
            
        except:
            pass
            
            
    bestFriends = {}
            
    for user, subUserDict in userScore.iteritems():
        maxScore = 0
        maxSubUser = ''
        bestScores = []
        
        for subUser, subUserScore in userScore[user].iteritems():
            if subUserScore > maxScore:
                maxScore = subUserScore
                maxSubUser = subUser
                
        if maxSubUser != '':
            #bestFriends[translator[user]] = translator[maxSubUser]
            #bestScores[translator[user]] = maxScore
            bestScores.append(translator[maxSubUser])
            bestScores.append(maxScore)
            bestFriends[translator[user]] = bestScores
    
    return bestFriends
    #return bestFriends, bestScores        
            

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
