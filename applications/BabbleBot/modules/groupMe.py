#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gluon import *
import requests
import subprocess
import os


# GLOBALS
progression = {}
finished = {}

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

def fileInfo(auth,id):
    #checks if we have file
    fileExists = os.path.isfile('/GroupMeDir/'+str(id))

    # find total amount of comments of group
    totalComments = totalCommentsInGroup(auth,id)
    comments = 0
    if fileExists:
        # TODO once files are created
        comments = 100
    else:
        comments = totalComments
    # returns T/F, and # of comments need to be updated
    return [fileExists,comments]

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

def isThread(auth,id):
    # checks if instance of downloadFromAPI is occuring.
    if id in finished:
        return True

def downloadFromAPI(auth,id, isFile,max):
    global progression
    global finished
    finished[id] = False
    progression[id] = 0
    
    if isFile == False:
        # if No File, download EVERYTHING!
        # create file
        writer = open("groupMeDir/" + id,"wa")
        # start progression from 0
        progression[id] = 0
        allComments = {}
        beforeID = ''
        for x in range(max,0,-1):
            output = requests.get("htpps://api.groupme.com/v3/groups/"+id+"/messages?token="+auth+";limit=1;before_id=" + beforeID)
            output = output.json()
            #update beforeID
            beforeID = output['response']['messages']['id']
            #populate the dictionary
            allComments[x] = output['response']['messages']
            # increase progression
            progression[id] += 1
        # all comments in the DICT
        # write Dict to FILE!
        for key,value in allComments.iteritems():
            json.dump(value,writer)
    else:
        # file exists, get last message timestamp. Go till then
        writer = open("groupMeDir/" + id,"w")
        pass
    # Say we are done!
    finished[id] = True
    
def checker(id):
    global progression
    global finished
    prog = progress[id]
    fini = finished[id]
    if fini == True:
        # its finished!
        # delete values!
        del prog[id]
        del fini[id]
        return True
    # not finished
    return [False,prog]
