#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gluon import *
import os
import json
import markovify

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

def getBasicUserInfo(comments,userID):
    # Get # of comments, # of likes rec, likes given, likes/comment
    numComments = 0
    likesRec = 0
    likesGive = 0
    for k,val in comments.iteritems():
        try:
            v = json.loads(val)
            # count comments by user
            if v['user_id'] == userID:
                numComments += 1
                likesRec += int(len(v['favorited_by']))
            else:
                if userID in v['favorited_by']:
                    likesGive += 1
        except:
            pass
    return [numComments,likesRec,likesGive]

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

def countCommentsPerUser(comments, userID = 'ALL'):
    user = {}
    specificCount = 0
    for k,val in comments.iteritems():
        try:
            v = json.loads(val)
            if userID == 'ALL':
                if v['sender_id'] in user:
                    user[v['sender_id']] += 1
                else:
                    user[v['sender_id']] = 1
            else:
                if v['sender_id'] == userID:
                    specificCount += 1
        except:
            pass
    if userID == 'ALL':
        return user
    else:
        return specificCount

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

def mostGivingUsers(com, translator, personID = 'ALL'):
    # most like giving user!
    userDict = {}
    specificUser = 0
    for k,val in com.iteritems():
        try:
            v = json.loads(val)
            for x in v['favorited_by']:
                if personID == 'ALL':
                    if x in userDict:
                        userDict[x] += 1
                    else:
                        userDict[x] = 1
                elif x == personID:
                    specificUser += 1
        except:
            pass
    namedDict = {}
    for k, val in userDict.iteritems():
        if k in translator:
            namedDict[translator[k]] = val

    if personID == 'ALL':
        return namedDict
    else:
        return specificUser

def getMedalCount(user, com, translator, userCount):
    #Gets medal counts for each user
    userDict = {}
    #Set up return dictionary
    for k, val in translator.iteritems():
        medalDict = {'Platinum' : 0, 'Gold' : 0, 'Silver' : 0, 'Bronze' : 0}
        # Get # of active users
        userDict[k] = medalDict

    platinum = userCount
    gold =  int(userCount * .75)
    silver = int(userCount * .5)
    bronze = int(userCount * .25)

    for k,val in com.iteritems():
        try:
            v = json.loads(val)
            if v['sender_id'] in userDict:
                numFavorites = int(len(v['favorited_by']))
                medalDict = userDict[v['sender_id']]
                if numFavorites >= platinum:
                    userDict[v['sender_id']]['Platinum'] += 1
                elif numFavorites >= gold:
                    userDict[v['sender_id']]['Gold'] += 1
                elif numFavorites >= silver:
                    userDict[v['sender_id']]['Silver'] += 1
                elif numFavorites >= bronze:
                    userDict[v['sender_id']]['Bronze'] += 1

        except:
            pass

    namedDict = {}
    if user != "":
        namedDict[translator[user]] = userDict[user]
    else:
        for k, val in userDict.iteritems():
            if k in translator:
                namedDict[translator[k]] = val

    return namedDict,[platinum,gold,silver,bronze]
