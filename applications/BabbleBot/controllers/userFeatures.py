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
    richR = []
    for x in response:
        richR.append(session.translator[personID] + ' Markov Chain: ' + x)
    return dict(r=response, name = session.translator[personID], rich = richR)

def userLikesGiven():
    personID = request.vars.id
    response = groupMeFeatures.mostGivingUsers(session.dictComments,session.translator,personID)
    richResponse = session.translator[personID] + " Has Liked " + str(response) + " Other Messages!"
    return dict(r=response, name =session.translator[personID], rich = richResponse)

  def userCountComments():
    personID = request.vars.id
    response = groupMeFeatures.countCommentsPerUser(session.dictComments,personID)
    return dict(r=response, name = session.translator[personID])

def userMedals():
    personID = request.vars.id
    userDict = str(groupMeFeatures.getMedalCount(personID, session.dictComments, session.translator))
    return dict(m=userDict)
