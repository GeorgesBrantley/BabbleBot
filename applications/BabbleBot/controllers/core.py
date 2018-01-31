# -*- coding: utf-8 -*-
import groupMe
import thread

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
    fileFound,comments = groupMe.fileInfo(session.myAuth, session.myGroupID)
    session.fileFound = fileFound
    session.maxComments = comments
    # Function2: download comments THREAD?
    # work out method for progress bar (start a clock in GroupMe, 
    # Returns groupname, filefound, and # of comments needed
    return dict(name="test",fileFound=False, comments=comments)

def downloadComments():
    # start wheel if first time
    if not groupMe.isThread(session.myAuth, session.myGroupID):
        thread.start_new_thread(groupMe.updateComments, (session.myAuth, session.myGroupID, session.fileFound, session.maxComments,))
    # is it done? Check the ticker
    finished,prog = groupMe.checker(session.myGroupID)

    if finished:
        # If done!
        # Code to save dictionary...
        return dict(finished=True, prog=session.maxComments,max=session.maxComments)
    else:
        return dict(finished=False, prog=prog ,max=session.maxComments)

    return dict()

def featureList():
    #GroupMe api function, returns dictionary of information
    #HTML is a list of features to links, new controller?
    # dictionary saved to session?
    return dict()
