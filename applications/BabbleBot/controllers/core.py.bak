# -*- coding: utf-8 -*-
import groupMe
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
    groupID = request.vars.groupID
    botID = request.vars.botID
    auth = groupMe.checkValidAuth(personAuth)
    group = False
    if auth == True:
        group = groupMe.checkValidGroupID(personAuth,groupID)
    # if both are true:
    if auth == True and group == True:
        # save into sessions
        session.myAuth = personAuth
        session.myGroupID = groupID
        session.myBotID = botID
        name = groupMe.getGroupName(personAuth,groupID)
    return dict(auth=auth,group=group, name=name)

# Download Comments
def getComments():
    # Call GroupMeAPI functions
    # Function1: check if file exists / find last comment
    fileFound,totalComments,newComments = groupMe.fileInfo(session.myAuth, session.myGroupID)
    session.fileFound = fileFound
    session.maxComments = totalComments
    # Function2: download comments THREAD?
    # work out method for progress bar (start a clock in GroupMe, 
    # Returns groupname, filefound, and # of comments needed
    return dict(name="test",fileFound=fileFound, comments=newComments)

def downloadComments():
    # start wheel if first time
    if not groupMe.isThread(session.myAuth, session.myGroupID):
        thread.start_new_thread(groupMe.downloadFromAPI, (session.myAuth, session.myGroupID, session.fileFound, session.maxComments,))
        time.sleep(1)
    # is it done? Check the ticker
    finished,prog = groupMe.checker(session.myGroupID)

    if finished:
        session.dictComments = groupMe.getComments(session.myGroupID)
    return dict(finished=finished, prog= prog, max=session.maxComments)

def featureList():
    #GroupMe api function, returns dictionary of information
    #HTML is a list of features to links, new controller?
    # dictionary saved to session?
   
    com = session.dictComments
    # example for json
    comments = []
    for k,val in com.iteritems():
        try:
            v = json.loads(val)
            comments.append(v['text'].encode("utf-8") +'\n')
        except:
            pass
    return dict(com = comments)
