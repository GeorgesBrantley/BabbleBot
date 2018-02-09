# -*- coding: utf-8 -*-
import groupMe
import groupMeFeatures

# try something like
def index(): return dict(message="hello from features.py")

def likesPerUser():
    userDict = str(groupMeFeatures.getLikesPerUser(session.dictComments, session.translator))
    return dict(m=userDict)
