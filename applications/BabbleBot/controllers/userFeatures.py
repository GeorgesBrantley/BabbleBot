# -*- coding: utf-8 -*-
import groupMeFeatures
# All user features!

def main():
    # Page that displayes user name, and link to all user features
    personID = request.vars.id
    name = session.translator[personID]
    return dict(p=personID, n = name)

def userMarkov():
    personID = request.vars.id
    response = groupMeFeatures.createMarkChain(personID,10,session.dictComments)
    return dict(r=response, name = session.translator[personID])

def userSpecificLikes():
    personID = request.vars.id
    userDict = str(groupMeFeatures.specificLikesGiven(session.dictComments, session.translator, translator[personID]))
    return dict(m=userDict)

def userSpecificLikesRec():
    personID = request.vars.id
    userDict = str(groupMeFeatures.specificLikesRec(session.dictComments, session.translator, translator[personID]))
    return dict(m=userDict)
