# -*- coding: utf-8 -*-
import groupMe
import groupMeFeatures
import time
import json
import pDB

# Get information from Guest
def guestSignIn():
    #Form in html
    redirect(URL('auth','index'))

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
    # Get GroupID, fileFound, Max Comments, groupName
    groupID = request.vars.groupID
    #OPEN AND CLOSE
    flag = False # IF FILE EXISTS
    try:
        pDB.decrypt(groupID+session.email,session.uKey)
        flag = True
    except:
        pass
    fileFound,totalComments,newComments = groupMe.fileInfo(session.myAuth, groupID,session.email,session.uKey)
    if fileFound:
        try:
            pDB.encrypt(groupID+session.email,session.uKey)
        except:
            pass
    session.myGroupID = groupID
    session.fileFound = fileFound
    session.maxComments = totalComments
    name = groupMe.getGroupName(session.myAuth, groupID)
    session.groupName =  name
    # get comments!
    fileName = groupID + session.email
    if fileFound:
        try:
            pDB.decrypt(fileName,session.uKey)
        except:
            pass
    session.dictComments = groupMe.downloadFromAPI(session.myAuth, session.myGroupID,session.fileFound, session.maxComments, session.email, session.uKey)
    pDB.encrypt(fileName,session.uKey)

    translate = {}
    for k,val in session.dictComments.iteritems():
        try:
            v = json.loads(val)
            translate[v['user_id']] = str(v['name'].encode('utf-8'))
        except:
            pass
    session.translator = translate
    redirect(URL('featureList'))

def downloadCommentsGuest():
    # Get GroupID, fileFound, Max Comments, groupName
    groupID = request.vars.groupID
    session.fileFound = False
    session.myGroupID = groupID
    session.maxComments = groupMe.totalCommentsInGroup(session.myAuth, groupID)

    name = groupMe.getGroupName(session.myAuth, groupID)
    session.groupName =  name
    # get comments!

    session.dictComments = groupMe.downloadFromAPI(session.myAuth, session.myGroupID, session.fileFound, session.maxComments, 'Guest', session.uKey)

    translate = {}
    for k,val in session.dictComments.iteritems():
        try:
            v = json.loads(val)
            translate[v['user_id']] = str(v['name'].encode('utf-8'))
        except:
            pass
    session.translator = translate
    redirect(URL('featureList'))

def featureList():
    # Lists GLobal Features and Users!
    # Get Users
    users = [] # These are objects of [id,name]
    users = groupMe.getListOfUsers(session.myAuth, session.myGroupID)
    # basic data for display
    numLikes,numComs = groupMeFeatures.getBasicGroupInfo(session.dictComments)
    # number of comments total
    info = 'Total Number of Comments: ' + str(numComs) + '\nTotal Number of Likes: ' + str(numLikes)
    return dict(name = session.groupName,users=users,nLikes = numLikes, nComs = numComs, infoStr=info, email=session.email)

def postToGroupMe():
    message = request.vars.message
    botID = ''
    # In Database?
    botidDB = pDB.getGroupBot(session.myGroupID)

    if botidDB:
        # In database
        session.myBotID = botidDB['botID']
        # Post to GroupMe
    else:
        # Not in Database
        # Make Bot, Add it
        # GET BOTID
         redirect(URL('botPrompt', vars=dict(msg=message)))

    works = groupMe.postToGroupMe(session.myBotID,message)
    return dict(w=works)


def makeBot():
    # Get Message
    # Get BotID
    botID = request.vars.botID
    message = request.vars.message
    # TODO IF BOTID SUCKS ADD ERROR
    # Make Bot if it works
    session.myBotID = botID
    pDB.makeGroupBot(session.myGroupID, session.myBotID)
    redirect(URL('postToGroupMe', vars=dict(message=message)))

def botPrompt():
    #Form in html
    msg = ''
    msg = request.vars.msg
    return dict(msg = msg)

def updateGroup():
    # FINDS new Comments
    # Get GroupID, fileFound, Max Comments, groupName
    groupID = session.myGroupID
    #OPEN AND CLOSE
    pDB.decrypt(groupID+session.email,session.uKey)
    fileFound,totalComments,newComments = groupMe.fileInfo(session.myAuth, groupID,session.email,session.uKey)
    pDB.encrypt(groupID+session.email,session.uKey)

    session.maxComments = totalComments
    name = groupMe.getGroupName(session.myAuth, groupID)
    session.groupName =  name
    # get comments!
    fileName = groupID + session.email
    pDB.decrypt(fileName,session.uKey)
    session.dictComments = groupMe.downloadFromAPI(session.myAuth, session.myGroupID,session.fileFound, session.maxComments, session.email, session.uKey)
    pDB.encrypt(fileName,session.uKey)
    translate = {}
    for k,val in session.dictComments.iteritems():
        try:
            v = json.loads(val)
            translate[v['user_id']] = str(v['name'].encode('utf-8'))
        except:
            pass
    session.translator = translate
    redirect(URL('featureList'))

def bigUpdate():
    # removes files, and then redownloads
    pDB.refreash(session.myGroupID + session.email)
    session.dictComments = {}
    session.fileFound = False
    session.maxComments = 0
    session.translator = {}
    # Get GroupID, fileFound, Max Comments, groupName
    groupID = request.vars.groupID
    #OPEN AND CLOSE
    fileFound,totalComments,newComments = groupMe.fileInfo(session.myAuth, session.myGroupID,session.email,session.uKey)
    session.fileFound = fileFound
    session.maxComments = totalComments
    session.dictComments = groupMe.downloadFromAPI(session.myAuth, session.myGroupID,session.fileFound, session.maxComments, session.email, session.uKey)
    fileName = session.myGroupID + session.email
    pDB.encrypt(fileName,session.uKey)
    translate = {}
    for k,val in session.dictComments.iteritems():
        try:
            v = json.loads(val)
            translate[v['user_id']] = str(v['name'].encode('utf-8'))
        except:
            pass
    session.translator = translate
    redirect(URL('featureList'))

def smartUpdate():
    # Update last 100 comments

    # Update Comments
    fileName = session.myGroupID + session.email
    pDB.decrypt(fileName,session.uKey)
    session.dictComments = groupMe.smartUpdate(session.myAuth, session.myGroupID, session.email)
    pDB.encrypt(fileName,session.uKey)
    # The Dict Comments has been updated with the past 100 comments being revisted
    redirect(URL('featureList'))

def delGroup():
    pDB.refreash(session.myGroupID + session.email)
    session.dictComments = {}
    session.fileFound = False
    session.myGroupID = ''
    session.maxComments = 0
    session.translator = {}
    redirect(URL('auth','chooseGroup'))

def updateBot():
    oldBot= pDB.getGroupBot(session.myGroupID)
    if oldBot == False:
        redirect(URL('botPrompt'))
    else:
        return dict(botID = oldBot['botID'], groupN = session.groupName )

def newBot():
    newBotID = request.vars.newBotID
    update = pDB.updateGroupBot(session.myGroupID, newBotID)
    return dict(success = update, newBot = newBotID, groupN = session.groupName)
