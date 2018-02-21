# -*- coding: utf-8 -*-
import groupMe
import groupMeFeatures
import thread
import time
import json

# Get information from Guest
def guestSignIn():
    #Form in html
    return dict()

# Compute information from guestSignIn
def guestCheck():
    # Get information
    personAuth = request.vars.auth
    botID = request.vars.botID
    auth = groupMe.checkValidAuth(personAuth)
    group = False
    name = ''
    groups = []
    if auth == True:
        # save into sessions
        session.myAuth = personAuth
        session.myBotID = botID
        groups = groupMe.getAllGroups(personAuth)
    return dict(auth=auth,groups=groups)

# Download Comments
def getComments():
    # Call GroupMeAPI functions
    # Function1: check if file exists / find last comment
    groupID = request.vars.groupID
    # group = groupMe.checkValidGroupID(personAuth,groupID)

    # if group == true:
    fileFound,totalComments,newComments = groupMe.fileInfo(session.myAuth, groupID)
    session.myGroupID = groupID
    session.fileFound = fileFound
    session.maxComments = totalComments
    name = groupMe.getGroupName(session.myAuth, groupID)
    session.groupName =  name

    return dict(name=name,fileFound=fileFound,comments=newComments)

def downloadComments():
    # start wheel if first time
    if not groupMe.isThread(session.myAuth, session.myGroupID):
        thread.start_new_thread(groupMe.downloadFromAPI, (session.myAuth, session.myGroupID, session.fileFound, session.maxComments,))
        time.sleep(1)
    # is it done? Check the ticker
    finished,prog = groupMe.checker(session.myGroupID)

    if finished:
        session.dictComments = groupMe.getComments(session.myGroupID)
        com = session.dictComments
        translate = {}
        for k,val in com.iteritems():
            try:
                v = json.loads(val)
                translate[v['user_id']] = str(v['name'].encode('utf-8'))
            except:
                pass
        session.translator = translate
    return dict(finished=finished, prog= prog, max=session.maxComments)

def featureList():
    # Lists GLobal Features and Users!
    # Get Users
    users = [] # These are objects of [id,name]
    users = groupMe.getListOfUsers(session.myAuth, session.myGroupID)
    # basic data for display
    numLikes,numComs = groupMeFeatures.getBasicGroupInfo(session.dictComments)
    # number of comments total
    info = 'Total Number of Comments: ' + str(numComs) + '\nTotal Number of Likes: ' + str(numLikes) 
    return dict(name = session.groupName,users=users,nLikes = numLikes, nComs = numComs, infoStr=info)

def postToGroupMe():
    message = request.vars.message
    works = ''
    if session.myBotID is not '':
        works = groupMe.postToGroupMe(session.myBotID,message)
    return dict(w=works)
