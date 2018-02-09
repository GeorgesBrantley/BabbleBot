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
    botID = request.vars.botID
    auth = groupMe.checkValidAuth(personAuth)

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
#     group = groupMe.checkValidGroupID(personAuth,groupID)

    # if group == true:
    fileFound,totalComments,newComments = groupMe.fileInfo(session.myAuth, groupID)
    session.myGroupID = groupID
    session.fileFound = fileFound
    session.maxComments = totalComments
    name = groupMe.getGroupName(session.myAuth, groupID)

    # Function2: download comments THREAD?
    # work out method for progress bar (start a clock in GroupMe,
    # Returns groupname, filefound, and # of comments needed
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
