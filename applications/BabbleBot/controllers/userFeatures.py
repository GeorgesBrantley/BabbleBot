# -*- coding: utf-8 -*-
import groupMeFeatures
import groupMeFeaturesMatt
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
    for k,v in sorted(userDict[0].items(), key=lambda x: x[1], reverse=True):
        richResponse += " "+k + ': ' + str(v) + ' Comments Liked\n'
    return dict(m=userDict, n = name,rich = richResponse)

def userSpecificLikesRec():
    # Likes Recieved, ADMIRERS
    personID = request.vars.id
    name = session.translator[personID]
    userDict = groupMeFeatures.specificLikesRec(session.dictComments, session.translator, personID )

    richResponse = name + "'s Secret Admirers (Who likes " + name + "?): \n\n"
    for k,v in sorted(userDict[0].items(), key=lambda x: x[1], reverse=True):
        richResponse += " "+k + ': ' + str(v) + ' Comments Liked\n'
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

def userCurseWords():
    curseWords = groupMeFeaturesMatt.getCommonCurseWords(session.dictComments, session.translator, request.vars.id)
    richResponse = 'Most common curse words in group:\n\n'
    count = 0
    for word, list in sorted(curseWords.iteritems(), key=lambda x: x[0], reverse=True):
        number = list[0]
        if count <= 2:
            richResponse += word + ': ' + str(number) + ' \n'
        count += 1
    richResponse += '\n'

    return dict(u=session.translator[request.vars.id], m=curseWords, rich = richResponse)

def userMostLikedComments():
    # user's most liked comments
    personID = request.vars.id
    name = session.translator[personID]
    userDict = groupMeFeatures.getMostLikedComments(session.dictComments, session.translator, personID)
    richResponse = name + '\'s Top 10 Most Liked Comments:\n\n'
    x = 0
    summedComments = []
    for k,v in sorted(userDict.items(), key=lambda x:x[1][1], reverse=True):
        richResponse +=  str(v[1]) + ' Likes: ' + v[0].encode('utf-8') +  '\n\n'
        summedComments.append([v[0],v[1]])
        x += 1
        if x > 9:
            break
    return dict(n= name, m=summedComments, rich = richResponse)
