# -*- coding: utf-8 -*-
# try something like
import groupMeFeatures

def index(): return dict(message="hello from features.py")

def numComments():
    coms = session.dictComments
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
