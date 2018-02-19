#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gluon import *
import os
import json
import markovify
import types

def getBasicGroupInfo(comments):
    # total likes in a group
    # total comments in a group
    sumLikes = 0
    sumComments = 0
    for k,val in comments.iteritems():
        try:
            v = json.loads(val)
            # operate on v
            # find out amount of likes on this comment
            # add to sumLikes
            sumLikes = sumLikes + len(v["favorited_by"])
            # make sure only count human messages
            if v['sender_type'] == 'user':
                sumComments += 1
        except:
            pass
    return [sumLikes,sumComments]

def createMarkChain(user,amount,comments):
    # Gets user id, amount of chains to generate, and comments dictionary
    # if user = 'all', then we are getting the comments for everyone in the group!
    inputStr = ''
    # get comments
    for k,val in comments.iteritems():
        try:
            v = json.loads(val)
            # check of id
            if user == 'all' and v['sender_type'] == 'user':
                # grab everyone (thats not admin)
                string = v['text'].encode("utf-8")
                if string[-1:] != '.':
                    # add period if none
                    string += '.'
                inputStr += string +'\n'
            elif v['user_id'] == user:
                # TODO, opnly get that specific users comments
                string = v['text'].encode("utf-8")
                if string[-1:] != '.' and string[-1:] != '?' and string[-1:] != '!':
                    string += '.'
                inputStr += string +'\n'
        except:
            pass
    # make text model
    text_model = markovify.Text(inputStr)
    
    #create list of output
    outStr = []
    for i in range(0,amount):
        marky = text_model.make_sentence()
        pings = 0
        while marky == None or marky == 'None':
            if pings > 10:
                break
            marky = text_model.make_sentence()
        outStr.append(marky)
        
    # returns list of markov strings
    return outStr

def getLikesPerUser(com, translator):
    # Gets likes RECIEVED per user!
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
    for k, val in userDict.iteritems():
        if k in translator:
            namedDict[translator[k]] = val

    return namedDict

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

def mostGivingUsers(com, translator):
    # most like giving user!
    userDict = {}
    for k,val in com.iteritems():
        try:
            v = json.loads(val)
            for x in v['favorited_by']:
                # x is an ID in the favby list
                if x in userDict:
                    userDict[x] += 1
                else:
                    userDict[x] = 1
        except:
            pass
    namedDict = {}
    for k, val in userDict.iteritems():
        if k in translator:
            namedDict[translator[k]] = val

    return namedDict

def specificLikesGiven(com, translator, user = 'ALL'):
    # WHO DOES A USER LIKE SPECIFICALLY?
    userDict = {}
    for k,val in com.iteritems():
        try:
            v = json.loads(val)
            #userDict[v['sender_id']] = {}
            #print v['favorited_by']
            for x in v['favorited_by']:
                # x is an ID in the favby list
                try:
                    userDict[x]
                except:
                    userDict[x] = {}

                if v['sender_id'] in userDict[x]:
                    userDict[x][v['sender_id']] += 1
                else:
                    userDict[x][v['sender_id']] = 1
        except:
            pass

    namedDict = {}
    for k, val in userDict.iteritems():
        # iterate through users
        if k in translator:
            newVal = {}
            for kk,v in val.iteritems():
                # iterate through admirers
                newVal[translator[kk]]  = v
            namedDict[translator[k]] = newVal

    if user == 'ALL':
        return namedDict
    else:
        return namedDict[user]

def specificLikesRec(com, translator, user = 'ALL'):
    # WHO HAS LIKED THIS USER?
    userDict = {}
    for k,val in com.iteritems():
        try:
            v = json.loads(val)
            #userDict[v['sender_id']] = {}
            for x in v['favorited_by']:
                # x is an ID in the favby list
                try:
                    userDict[v['sender_id']]
                except:
                    userDict[v['sender_id']] = {}

                if x in userDict[v['sender_id']]:
                    userDict[v['sender_id']][x] += 1
                else:
                    userDict[v['sender_id']][x] = 1
        except:
            pass

    namedDict = {}
    for k, val in userDict.iteritems():
        # iterate through users
        if k in translator:
            newVal = {}
            for kk,v in val.iteritems():
                # iterate through admirers
                newVal[translator[kk]]  = v
            namedDict[translator[k]] = newVal
    if user == 'ALL':
        return namedDict
    else:
        return namedDict[user]
