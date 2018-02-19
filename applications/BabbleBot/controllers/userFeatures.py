# -*- coding: utf-8 -*-
import groupMeFeatures
# All user features!

def main():
    # Page that displayes user name, and link to all user features
    personID = request.vars.id
    name = session.translator[personID]
    # Get number of comments, likes given, likes recieved, likes/comment
    numComs,likesGiven,likesRec = groupMeFeatures.getBasicUserInfo(session.dictComments,personID)
    ratio = float(likesRec) / numComs
    ratio = round(ratio,2)
    richResponse = []
    richResponse.append(name + ' Has Posted ' + str(numComs) + ' Coments!')
    richResponse.append(name + ' Has Recieved ' +str(likesRec)+ ' Likes!')
    richResponse.append(name + ' Has Given ' + str(likesGiven) + ' Likes!')
    richResponse.append(name + ' Has a Likes/Comment Ratio of ' +str(ratio) + ' Likes!')
    print str(richResponse)
    return dict(p=personID, group = session.groupName, n = name, numComs=numComs, likesGiven=likesGiven, likesRec=likesRec, ratio=ratio, rResponse = richResponse)

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

def userSpecificLikes():
    personID = request.vars.id
    userDict = str(groupMeFeatures.specificLikesGiven(session.dictComments, session.translator, translator[personID]))
    return dict(m=userDict)

def userSpecificLikesRec():
    personID = request.vars.id
    userDict = str(groupMeFeatures.specificLikesRec(session.dictComments, session.translator, translator[personID]))
    return dict(m=userDict)

def userMedals():
    personID = request.vars.id
    numUsers = len(groupMe.getListOfUsers(session.myAuth,session.myGroupID))
    userDict = str(groupMeFeatures.getMedalCount(personID, session.dictComments, session.translator),numUsers)
    return dict(m=userDict)
