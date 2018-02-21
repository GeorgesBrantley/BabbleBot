#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gluon import *
import requests
import subprocess
import os
import json
import copy

# GLOBALS
progression = {}
finished = {}
commentsDicts = {}

def checkValidAuth(auth):
    # checks if auth inputed is legit
    output = requests.get("https://api.groupme.com/v3/groups?token=" + auth)
    if str(output.status_code) == '200':
        return True
    else:
        return False

def checkValidGroupID(auth,groupID):
    # checks if groupID is legit
    output = requests.get("https://api.groupme.com/v3/groups/"+groupID+"?token=" + auth)
    if str(output.status_code) == '200':
        return True
    else:
        return False

def getListOfUsers(auth,groupID):
    # gets users of a group [id,nickname]
    req = requests.get("https://api.groupme.com/v3/groups/"+groupID+"?token=" + auth)
    output = req.json()
    names = output['response']['members']
    users = []
    for x in names:
        users.append([x['user_id'],x['nickname']])
    return users

def fileInfo(auth,groupid):
    #checks if we have file
    f = None
    try:
        f = open('GroupMeDir/'+str(groupid),'r')
        fileExists = True
    except:
        fileExists = False
    # find total amount of comments of group
    totalComments = totalCommentsInGroup(auth,groupid)
    newcomments = 0
    if fileExists:
        jj = json.load(f)
        oldComments = jj['LASTCOUNT']
        newcomments = int(totalComments) - int(oldComments)
    else:
        newcomments = totalComments
    # returns T/F, and # of comments need to be updated
    return [fileExists,totalComments, newcomments]

def totalCommentsInGroup(auth,id):
    output = requests.get("https://api.groupme.com/v3/groups/"+id+"?token=" + auth)
    output = output.json()
    totalComments = output['response']['messages']['count']
    return int(totalComments)

def getGroupName(auth,id):
    output = requests.get("https://api.groupme.com/v3/groups/"+id+"?token=" + auth)
    output = output.json()
    name = output['response']['name']
    return name

# Gets all the groups a user is in
def getAllGroups(auth):
    # the omit=memberships will exclude the list of all the group members, which is good for people in large groups.
    output = requests.get("https://api.groupme.com/v3/groups?token=" + auth + "&omit=memberships")
    output = output.json()
    groups = output['response']
    return groups

def isThread(auth,id):
    # checks if instance of downloadFromAPI is occuring.
    if id in finished:
        return True

def downloadFromAPI(auth,groupID, isFile,maxCom):
    global progression
    global finished
    global commentsDicts
    finished[groupID] = False
    progression[groupID] = 0
    
    if isFile == False:
        # if No File, download EVERYTHING!
        # create file
        writer = open("GroupMeDir/" + groupID,"w+")
        writer = open("GroupMeDir/" + groupID,"wa")
        # start progression from 0
        progression[groupID] = 0
        allComments = {}
        beforeID = ''
        firstID = ''
        for x in range(maxCom,0,-1):
            output = requests.get("https://api.groupme.com/v3/groups/"+groupID+"/messages?token="+auth+";limit=1;before_id=" + beforeID)
            output = output.json()
            #update beforeID
            for y in output['response']['messages']:
                if beforeID == '':
                    firstID = y['id']
                beforeID = y['id']
            #populate the dictionary
            allComments[x] = json.dumps(output['response']['messages'][0])
            # increase progression
            progression[groupID] += 1
            #update last count
        # all comments in the DICT
        # Stores the last comment (most recent posted) 's ID. for dif equations
        allComments['LASTID'] = firstID
        allComments['LASTCOUNT'] = maxCom #stores the max comment values
        # write Dict to FILE! NO ORDER (by ID though)
        json.dump(allComments,writer)
        commentsDicts[groupID] = allComments
    else:
        # file exists, get last message timestamp. Go till then
        writer = open("GroupMeDir/" + groupID,"r")
        jj = json.load(writer)
        ## jj is the json object. need to figure out how to read through it
        lastID = jj['LASTID'] # finds the last comment id
        oldMax = int(jj['LASTCOUNT']) # the dictionary # of last comment
        beforeID = ''
        firstID = ''
        newComments = {}
        for x in range(maxCom,oldMax,-1): # Goes from New MAX comments, to the old max
            output = requests.get("https://api.groupme.com/v3/groups/"+groupID+"/messages?token="+auth+";limit=1;before_id=" + beforeID)
            output = output.json()
            for y in output['response']['messages']:
                if beforeID == '':
                    firstID = y['id']
                beforeID = y['id']
            if beforeID == lastID:
                # We caught up! Do not add this to New Comments
                break
            else:
                # Catching up... add to new Comments
                newComments[x] = json.dumps(output['response']['messages'][0])
            progression[groupID] += 1
        # NewComments now is a dict of new comments, need to join with comments in file.

        # Read comments in file, add to new Comments
        for x in range(oldMax, 0, -1):
            oldComment = json.loads(jj[str(x)])
            try:
                oldComment = oldComment[0]
            except:
                pass
            newComments[x] = json.dumps(oldComment)
        # Overright JSON file
        subprocess.check_output("echo '' > GroupMeDir/" + str(groupID),shell=True)
        writer = open("GroupMeDir/" + str(groupID), 'w')
        # all comments in the DICT
        # Stores the last comment (most recent posted) 's ID. for dif equations
        newComments['LASTID'] = firstID
        newComments['LASTCOUNT'] = maxCom #stores the previous last comment #
        # write Dict to FILE! NO ORDER (by ID though)
        json.dump(newComments,writer)
        commentsDicts[groupID] = newComments
        
    # Say we are done!
    finished[groupID] = True
    
def checker(groupID):
    global progression
    global finished
    prog = progression[groupID]
    fini = finished[groupID]
    if fini == True:
        # its finished!
        # delete values!
        del progression[groupID]
        del finished[groupID]
        return [True,100000]
    # not finished
    return [False,prog]

def getComments(groupID):
    # Returns dictionary of comments
    # DO NOT USE IN FEATURES!!!
    global commentsDicts
    ret = ''
    try:
        ret = copy.deepcopy(commentsDicts[groupID])
        del commentsDicts[groupID]
        # TODO, add AUTH CHECK!
    except:
        pass
    return ret


def postToGroupMe(botID, message):
    #Posts to the GroupMe associated with this Bot
    # Need to check if Message is too long... 9999 char limit!
    packages = []
    cut = 995
    while len(message) > cut:
        packages.append(message[:cut])
        message = message[cut:]
    packages.append(message)

    for x in packages:
        payload = {'bot_id':botID,'text':x}
        r = requests.post("https://api.groupme.com/v3/bots/post", data=payload)
    try:
        jj = json.loads(r.text)
        if jj['meta']['code'] == '404':
            return False
    except:
        return True
    return True
