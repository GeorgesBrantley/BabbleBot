# -*- coding: utf-8 -*-
import groupMeFeatures
import groupMe
# All user features!

def main():
    # Page that displayes user name, and link to all user features
    personID = request.vars.id
    name = session.translator[personID]
    # Get number of comments, likes given, likes recieved, likes/comment
    numComs,likesRec, likesGiven = groupMeFeatures.getBasicUserInfo(session.dictComments,personID)
    ratio = float(likesRec) / numComs
    ratio = round(ratio,2)
    richResponse = []
    richResponse.append(name + ' Has Posted ' + str(numComs) + ' Coments!')
    richResponse.append(name + ' Has Recieved ' +str(likesRec)+ ' Likes!')
    richResponse.append(name + ' Has Given ' + str(likesGiven) + ' Likes!')
    richResponse.append(name + ' Has a Likes/Comment Ratio of ' +str(ratio) + ' Likes!')
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
    response = groupMeFeatures.countCommentsPerUser(session.dictComments,session.translator, personID)
    return dict(r=response, name = session.translator[personID])

def userGetLikesPerComment():
    personID = request.vars.id
    response = groupMeFeatures.createMarkChain(session.dictComments,session.translator,personID)
    return dict(r=response)

def userSpecificLikes():
    # Likes Specifically Given, CRUSHES
    personID = request.vars.id
    name = session.translator[personID]
    userDict = groupMeFeatures.specificLikesGiven(session.dictComments, session.translator, personID)

    richResponse = name + "'s Secret Crushes (Who does " + name + " like?): \n\n"
    for k,v in sorted(userDict.items(), key=lambda x: x[1], reverse=True):
        richResponse += "\t"+k + ': ' + str(v) + ' Comments Liked\n'
    return dict(m=userDict, n = name,rich = richResponse)

def userSpecificLikesRec():
    # Likes Recieved, ADMIRERS
    personID = request.vars.id
    name = session.translator[personID]
    userDict = groupMeFeatures.specificLikesRec(session.dictComments, session.translator, personID )

    richResponse = name + "'s Secret Admirers (Who likes " + name + "?): \n\n"
    for k,v in sorted(userDict.items(), key=lambda x: x[1], reverse=True):
        richResponse += "\t"+k + ': ' + str(v) + ' Comments Liked\n'
    return dict(m=userDict, n = name,rich = richResponse)

def userMedals():
    personID = request.vars.id
    name = session.translator[personID]
    numUsers = len(groupMe.getListOfUsers(session.myAuth,session.myGroupID))
    userDict,medals = groupMeFeatures.getMedalCount(personID, session.dictComments, session.translator, numUsers)
    userDict = userDict[name]
    richResponse = name + "'s Earned Medals:\n"
    richResponse+= 'Platnium (' + str(numUsers) + ' likes): ' + str(userDict['Platinum'])
    richResponse+= '\nGold ('   + str(int(numUsers*.75)) + ' likes): ' + str(userDict['Gold'])
    richResponse+= '\nSilver (' + str(int(numUsers*.50)) + ' likes): ' + str(userDict['Silver'])
    richResponse+= '\nBronze (' + str(int(numUsers*.25)) + ' likes): ' + str(userDict['Bronze'])
    return dict(m=userDict, r=medals, n=name, rich = richResponse)
