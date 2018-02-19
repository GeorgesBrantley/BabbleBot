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

def userGetLikesPerComment():
    personID = request.vars.id
    response = groupMeFeatures.createMarkChain(session.dictComments,personID)
    return dict(r=response)
