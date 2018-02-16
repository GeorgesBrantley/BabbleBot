# -*- coding: utf-8 -*-
import groupMeFeatures
import groupMe
import operator

def sumOfLikesinGroup():
    # Has a corresponding view
    # gets values from Sessions
    comments = session.dictComments
    # sends values to bigger function in groupMeFeatures.py
    sumLikes = groupMeFeatures.getSumofLikes(comments)
    # shows output on view
    return dict(sum = sumLikes)

def groupMarkov():
    # Display Markov Chains for entire Group
    comments = session.dictComments # get comments
    results = groupMeFeatures.createMarkChain('all',10,comments)
    
    return dict(marks = results)


def likesRecievedPerUser():
    userDict = groupMeFeatures.getLikesPerUser(session.dictComments, session.translator)
    return dict(m=userDict)

def numComments():
    coms = session.dictComments
    #id = inout
    #inputId = 19191585
    ans = groupMeFeatures.countCommentsPerUser(coms)
    return dict(ans=ans)

def pastName():
    coms = session.dictComments
    ans = groupMeFeatures.getPastName(coms)
    return dict(PastName=ans)

def numKicked():
    coms = session.dictComments
    ans = groupMeFeatures.getNumKicked(coms)
    return dict(numKicked=ans)

def mostGivingUsers():
    userDict = groupMeFeatures.mostGivingUsers(session.dictComments, session.translator)
    return dict(m=userDict)
