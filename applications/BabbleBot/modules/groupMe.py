#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gluon import *
import requests
import subprocess
import os
import json
import copy
import sys
import pDB
import time

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
        users.append([x['user_id'],x['nickname'], x['image_url']])
    return users

def fileInfo(auth,groupid,email,uKey):
    #checks if we have file
    f = None
    fileName = groupid + email
    #if True:
    try:
        #DECRYPT
        f = open('GroupMeDir/'+fileName ,'r')
        fileExists = True
    except:
        fileExists = False
    # find total amount of comments of group
    totalComments = totalCommentsInGroup(auth,groupid)

    newcomments = 0
    if fileExists:
        try:
            jj = json.load(f)
        except:
            # Error with file, delete files, return false
            pDB.refreash(fileName)
            return [False,totalComments,totalComments]
        oldComments = jj['LASTCOUNT']
        newcomments = int(totalComments) - int(oldComments)
    else:
        newcomments = totalComments
    # returns T/F, and # of comments need to be updated
    try:
        f.close()
    except:
        pass
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

def downloadFromAPI(auth,groupID, isFile,maxCom,email,uKey):

    if isFile == False:
        # if No File, download EVERYTHING!
        # create file
        writer = open("GroupMeDir/" + groupID + email,"w+")
        writer = open("GroupMeDir/" + groupID + email,"wa")

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
            #update last count
        # all comments in the DICT
        # Stores the last comment (most recent posted) 's ID. for dif equations
        allComments['LASTID'] = firstID
        allComments['LASTCOUNT'] = maxCom #stores the max comment values
        # write Dict to FILE! NO ORDER (by ID though)
        json.dump(allComments,writer)
        #subprocess.check_output("cat GroupMeDir/39425744gbrantlepurdue.edu > GroupMeDir/test22", shell = True)
        # ENCRYPT
        #fileName = groupID + email
        #pDB.encrypt(fileName,uKey)
        return allComments
    else:
        # DECRYPT
        #fileName = groupID + email
        #pDB.decrypt(fileName,uKey)
        # file exists, get last message timestamp. Go till then
        writer = open("GroupMeDir/" + groupID + email,"r")
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
        subprocess.check_output("echo '' > GroupMeDir/" + str(groupID)+str(email),shell=True)
        writer = open("GroupMeDir/" + str(groupID) + str(email), 'w')
        # all comments in the DICT
        # Stores the last comment (most recent posted) 's ID. for dif equations
        newComments['LASTID'] = firstID
        newComments['LASTCOUNT'] = maxCom #stores the previous last comment #
        # write Dict to FILE! NO ORDER (by ID though)
        json.dump(newComments,writer)
        # ENCRYPT
        #pDB.encrypt(fileName,uKey)
        return newComments


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

def createBot(auth, groupID):
    print auth
    payload = {'bot' : {'name' : "BabbleBot", 'group_id' : groupID, 'callback_url': "https://google.com" }}
    url = "https://api.groupme.com/v3/bots?token=" + auth

    headers = {"Content-type": "application/json; charset=utf-8",  "Accept": "application/json"}
    print url
    response = requests.post(url, data=json.loads(str(payload)), headers=headers)
    print response
    print response.text
    try:
        jj = json.loads(response.text)
        print jj
        if jj['meta']['code'] == '404':
            print '404' + jj['response']
            return '404'
        elif jj['meta']['code'] == '500':
            print 500
        else:
            print "jj[resopnse]: " + jj['response']
            return jj['response']['bot']['bot_id']
    except:
        e = sys.exc_info()[1]
        print e
        return ''
