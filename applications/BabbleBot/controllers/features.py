# -*- coding: utf-8 -*-
import groupMeFeatures
import groupMe

def groupMarkov():
    # Display Markov Chains for entire Group
    comments = session.dictComments # get comments
    results = groupMeFeatures.createMarkChain('all',10,comments)
    
    return dict(marks = results)


def likesRecievedPerUser():
    userDict = str(groupMeFeatures.getLikesPerUser(session.dictComments, session.translator))
    return dict(m=userDict)
