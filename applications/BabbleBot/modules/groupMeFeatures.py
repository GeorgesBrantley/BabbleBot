#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gluon import *
import os
import json
import markovify

def getSumofLikes(comments):
    sumLikes = 0
    for k,val in comments.iteritems():
        try:
            v = json.loads(val)
            # operate on v
            comments.append(v['text'].encode("urf-8")+'\n')
            # find out amount of likes on this comment
            # add to sumLikes
            sumLikes = sumLikes + len(comment.get("favorited_by"))
        except:
            pass
    return sumLikes

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
                if string[-1:] != '.':
                    string += '.'
                inputStr += string +'\n'
        except:
            pass
    # make text model
    text_model = markovify.Text(inputStr)
    
    #create list of output
    outStr = []
    for i in range(0,amount):
        outStr.append(text_model.make_sentence())
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
