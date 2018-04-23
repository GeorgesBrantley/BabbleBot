#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gluon import *
import os
import json
import markovify
import types
import datetime
import pytz

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
            if v['sender_id'] == userID:
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
            if v['sender_type'] == 'user':
                if v['sender_id'] in userDict:
                    userDict[v['sender_id']] += int(len(v['favorited_by']))
                else:
                    userDict[v['sender_id']] = len(v['favorited_by'])
        except:
            pass
    nameDict = {}
    for k, val in userDict.iteritems():
        if k in translator:
            nameDict[translator[k]] = val
    return nameDict

def countCommentsPerUser(comments, translator, userID = 'ALL'):
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

    nameDict = {}
    for k, val in user.iteritems():
        if k in translator:
            nameDict[translator[k]] = val

    if userID == 'ALL':
        return nameDict
    else:
        return specificCount

def getPastName(comments):
    oldNames = []
    newNames = []
    for k,val in comments.iteritems():
        try:
            v = json.loads(val)
            if v['sender_id'] == 'system' and  'changed name to' in v['text'].encode("utf-8"):
                nameStr = v['text'].encode("utf-8")
                oldName = nameStr[:nameStr.find("changed name to ")-1]
                newName = nameStr[nameStr.find("changed name to ") + 16:]
                oldNames.append(oldName)
                newNames.append(newName)
        except:
            pass
    return oldNames,newNames

def getNumKicked(comments):
    kickers = {}
    kicked = {}
    for k,val in comments.iteritems():
        try:
            v = json.loads(val)
            if v['sender_id'] == 'system':
                kickStr = v['text'].encode("utf-8")
                if 'removed' in kickStr and 'changed the topic to:' not in kickStr:
                    kick = kickStr[:kickStr.find('removed') - 1]
                    if kick in kickers:
                        kickers[kick] += 1
                    else:
                        kickers[kick] = 1

                    victim = kickStr[kickStr.find('removed')+8:kickStr.find('from the group')-1]
                    if victim in kicked:
                        kicked[victim] += 1
                    else:
                        kicked[victim] = 1

        except:
            pass
    # kickers has a dicitonary of people who kick others
    # kicked has dicitonary of people who have been kicked
    return kickers,kicked

def mostGivingUsers(com, translator, personID = 'ALL'):
    # most like giving user!
    userDict = {}
    specificUser = 0
    for k,val in com.iteritems():
        try:
            v = json.loads(val)
            if v['sender_type'] == 'user':
                for x in v['favorited_by']:
                    # x is an ID in the favby list
                    if personID == 'ALL':
                        if x in userDict:
                            userDict[x] += 1
                        else:
                            userDict[x] = 1
                    elif x == personID:
                        specificUser += 1
        except:
            pass
    if personID == 'ALL':
        namedDict = {}
        for k, val in userDict.iteritems():
            if k in translator:
                namedDict[translator[k]] = val
        return namedDict
    else:
        return specificUser

def specificLikesGiven(com, translator, user = 'ALL'):
    # WHO DOES A USER LIKE SPECIFICALLY?
    userDict = {}
    numComments = {}
    for k,val in com.iteritems():
        try:
            v = json.loads(val)
            if v['sender_type'] == 'user':
                # GET COMMENTS NUMBER
                if v['sender_id'] in numComments:
                    numComments[v['sender_id']] += 1
                else:
                    numComments[v['sender_id']] = 1
                # GET LIKERS COOL
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
            namedDict[translator[k]] = [newVal,numComments[k]]

    if user == 'ALL':
        return namedDict
    else:
        return namedDict[translator[user]]

def specificLikesRec(com, translator, user = 'ALL'):
    # WHO HAS LIKED THIS USER?
    userDict = {}
    numComments = {}
    for k,val in com.iteritems():
        try:
            v = json.loads(val)
            if v['sender_type'] == 'user':
                # GET COMMENTS NUMBER
                if v['sender_id'] in numComments:
                    numComments[v['sender_id']] += 1
                else:
                    numComments[v['sender_id']] = 1
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
                if kk in translator:
                    newVal[translator[kk]]  = v
            namedDict[translator[k]] = [newVal,numComments[k]]
    if user == 'ALL':
        return namedDict
    else:
        return namedDict[translator[user]]

def getLikesPerComment(comments,translator, user = 'ALL'):
    # ratio of likes per comment
    usersDict = {}
    sumComments = 0
    sumLikes = 0
    for k,val in comments.iteritems():
        try:
            v = json.loads(val)
            # find number of likes per user
            if user == 'ALL':
                if v['sender_id'] in usersDict:
                    numComs, sumLikes,ratio = usersDict[v['sender_id']]
                    numComs += 1
                    sumLikes += len(v["favorited_by"])
                    ratio = sumLikes*1.0/numComs
                    usersDict[v['sender_id']] = [numComs, sumLikes, round(ratio,2)]
                else:
                    usersDict[v['sender_id']] = [1,len(v["favorited_by"]),len(v["favorited_by"])]
            else:
                if v['sender_id'] == user:
                    sumComments += 1
                    sumLikes += len(v["favorited_by"])
        except:
            pass
    if user != 'ALL':
        ratio = sumLikes/sumComments
        return ratio
    else:
        namedDict = {}
        for k,val in usersDict.iteritems():
            namedDict[translator[k]] = val[2]
        return namedDict

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
            if v['sender_type'] == 'user':
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

def getCommonCurseWords(com, translator, user = 'ALL'):
    curseWords = {' fuck': [0,{}], ' piss': [0,{}], ' shit' : [0,{}], ' damn' : [0,{}], ' ass' : [0,{}], ' dick' : [0,{}], ' bastard' : [0,{}], ' prick' : [0,{}], ' motherfucker' : [0,{}], ' gosh-golly' : [0,{}]}

    userDict = {}

    for k,val in com.iteritems():
        try:
            v = json.loads(val)
            for key in curseWords.keys():
                if key in v['text']:
                    curseWords[key][0] += 1
                    if not v['sender_id'] in curseWords[key][1]:
                        curseWords[key][1][v['sender_id']] = 0
                    curseWords[key][1][v['sender_id']] += 1


        except:
            pass

    print curseWords
    return curseWords

def getMostLikedComments(comments, translator, user = 'ALL'):
    likedCommentsDict = {}
    sumLikes = 0
    for k,val in comments.iteritems():
        try:
            v = json.loads(val)
            # global most liked comments
            if user == 'ALL' and v['sender_type'] == 'user':
                output = v['text']
                try:
                    output2 = v['attachments'][0]['url']
                    if output == None or output == 'None' or output == '':
                        likedCommentsDict[v['id']] = [output2, len(v['favorited_by']),v['sender_id']]
                    elif output2 != None and output2 != '' and output != output2:
                        likedCommentsDict[v['id']] = [output + ' -- ' + output2, len(v['favorited_by']),v['sender_id']]
                    else:
                        likedCommentsDict[v['id']] = [output, len(v['favorited_by']),v['sender_id']]
                except:
                    likedCommentsDict[v['id']] = [output, len(v['favorited_by']),v['sender_id']]

            # individual most liked comments
            elif v['user_id'] == user:
                output = v['text']
                try:
                    output2 = v['attachments'][0]['url']
                    if output == None or output == 'None' or output == '':
                        likedCommentsDict[v['id']] = [output2, len(v['favorited_by'])]
                    elif output2 != None and output2 != '' and output != output2:
                        likedCommentsDict[v['id']] = [output + ' -- ' + output2, len(v['favorited_by'])]
                    else:
                        likedCommentsDict[v['id']] = [output, len(v['favorited_by'])]
                except:
                    likedCommentsDict[v['id']] = [output, len(v['favorited_by'])]
        except:
            pass
    if user == 'ALL':
        for k,val in likedCommentsDict.iteritems():
            val[2] = translator[val[2]]
    return likedCommentsDict

def getSexismTracker(comments, translator, genderDict):
    userDict = {}
    sumMales = 0
    sumFemales = 0
    for k, val in comments.iteritems():
        try:
            v = json.loads(val)
            if v['sender_type'] == 'user':
                # check gender of sender and calculate total comments per gender
                if genderDict[v['sender_id']] == 'male':
                    sumMales += 1
                else:
                    sumFemales += 1
                # keep track of everyones # of comments
                if v['sender_id'] in userDict:
                    userDict[v['sender_id']][2] += 1
                else:
                    userDict[v['sender_id']] = [0,0,1]
                # check gender of 'likers' put into userDict
                for person in v['favorited_by']:
                    if person in userDict:
                        if genderDict[v['sender_id']] == 'male':
                            userDict[person][0] += 1
                        else:
                            userDict[person][1] += 1
                    else:
                        if genderDict[v['sender_id']] == 'male':
                            userDict[person] = [1, 0, 0]
                        else:
                            userDict[person] = [0, 1, 0]
        except:
            pass
    # calculate ratio of comments by males/females
    if sumFemales == 0 or sumMales == 0:
        return False

    ratio = sumMales * 1.0 / sumFemales
    # calculate actual ratio (per person) and give result
    resultDict = {}
    # result Dict -> list of users by ID (key)
    # [male likes, female likes, personal ratio, scaled ratio]
    for person,likes in userDict.iteritems():
        if likes[0] == 0 or likes[1] == 0:
            pass
        else:
            personalRatio = likes[0]*1.0/likes[1]
            # Make sure their comments are not used against them
            specRatio = ratio
            try:
                if genderDict[person] == 'male':
                    specRatio = (sumMales-likes[2]) *1.0/sumFemales
                else:
                    specRatio = sumMales*1.0/(sumFemales - likes[2])
            except:
                specRatio = ratio
            scaledRatio = round(personalRatio - specRatio,2)
            if scaledRatio > 8:
                color = '#641E16'
            elif scaledRatio > 4:
                color = '#922B21'
            elif scaledRatio > 2:
                color = '#C0392B'
            elif scaledRatio > 1:
                color = '#D98880'
            elif scaledRatio > .5:
                color = '#E6B0AA'
            elif scaledRatio > 0:
                color = '#F2D7D5'
            elif scaledRatio == 0:
                color = '#FFFFFF'
            elif scaledRatio > -.5:
                color = '#F4ECF7'
            elif scaledRatio > -1:
                color = '#E8DAEF'
            elif scaledRatio > -2:
                color = '#8E44AD'
            elif scaledRatio > -4:
                color = '#8E44AD'
            elif scaledRatio > -8:
                color = '#6C3483'
            else:
                color = '#4A235A'
            resultDict[person] = [likes[0], likes[1], personalRatio,scaledRatio,color]
    # translate userID to names

    namedDict = {}
    for k, val in resultDict.iteritems():
        if k in translator:
            namedDict[translator[k]] = val
    ratio = round(ratio,2)
    return [namedDict,ratio]

def getAllComments(comments, translator, user = 'ALL'):
    
    commentsDict= {}
    for k, val in comments.iteritems():
        try:
            v = json.loads(val)
            # global all comments
            if user == 'ALL' and v['sender_type'] == 'user':
                output = v['text']
                timeInt = v['created_at']
                #.strftime('%m-%d-%Y, %H:%M:%S'
                timeStamp = datetime.datetime.utcfromtimestamp(int(timeInt))
                newTime = timeStamp - datetime.timedelta(hours=4)
                timeStamp = newTime.strftime('%m-%d-%Y, %H:%M:%S')
                try:
                    output2 = v['attachments'][0]['url']
                    if output == None or output == 'None' or output == '':
                        commentsDict[v['id']] = [v['sender_id'], output2,timeStamp, len(v['favorited_by'])]
                    elif output2 != None and output2 != '' and output != output2:
                        commentsDict[v['id']] = [v['sender_id'], output + ' -- ' + output2, timeStamp, len(v['favorited_by'])]
                    else:
                        commentsDict[v['id']] = [v['sender_id'], output, timeStamp, len(v['favorited_by'])]
                except:
                    commentsDict[v['id']] = [v['sender_id'], output, timeStamp, len(v['favorited_by'])]
        except:
            pass
    for k, val in commentsDict.iteritems():
        if val[0] in translator:
            val[0] = translator[val[0]]
    return commentsDict
