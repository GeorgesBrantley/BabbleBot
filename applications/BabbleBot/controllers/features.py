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
    richResponse = []
    for x in results:
        richResponse.append('Group Markov Chain: ' + x)
    return dict(marks = results, rich = richResponse)


def likesRecievedPerUser():
    userDict = groupMeFeatures.getLikesPerUser(session.dictComments, session.translator)
    richResponse = 'Member Rankings by Total Likes Recieved:\n\n'
    for k,v in sorted(userDict.items(), key=lambda x: x[1], reverse=True):
        richResponse += k + ': ' + str(v) + ' Total Likes Recieved\n'
    return dict(m=userDict, rich = richResponse)

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
    kickers,kicked = groupMeFeatures.getNumKicked(coms)
    richV = 'List of Victims (Number of Times They\'ve Been Kicked):\n\n'
    richK = 'List of Bullies (Number of Times They Removed Someone):\n\n'
    for k,v in sorted(kickers.items(), key=lambda x: x[1], reverse=True):
        richK += " " + k + ": " + str(v) + " People Kicked\n"
    for k,v in sorted(kicked.items(), key=lambda x: x[1], reverse=True):
        richV += " " + k + ": " + str(v) + " Times Kicked\n"
    return dict(kickers=kickers,kicked=kicked, richVictim=richV, richKicker = richK)

def mostGivingUsers():
    userDict = groupMeFeatures.mostGivingUsers(session.dictComments, session.translator)
    richResponse = 'Member Rankings by Total Likes Given:\n\n'
    for k,v in sorted(userDict.items(), key=lambda x: x[1], reverse=True):
        richResponse += k + ': ' + str(v) + ' Total Likes Given\n'
    return dict(m=userDict, rich = richResponse)

def likesPerComment():
    ratio = groupMeFeatures.getLikesPerComment(session.dictComments,session.translator)
    richResponse = 'Member Rankings by Average Likes Per Comment:\n\n'
    for k,v in sorted(ratio.items(), key=lambda x: x[1], reverse=True):
        richResponse += k + ': ' + str(v) + ' Likes/Comment\n'
    return dict(m=ratio, rich = richResponse)

def specificLikes():
    # a user's secret crush
    userDict = groupMeFeatures.specificLikesGiven(session.dictComments, session.translator)
    richResponse = 'Secret Crushes (Who Users Like The Most):\n\n'
    for k,v in userDict.iteritems():
        richResponse += k + "'s Secret Crushes:\n"
        limit = 0
        for kk,vv in  sorted(v.items(), key=lambda x: x[1], reverse=True):
            limit += 1
            if limit > 3:
                break
            richResponse += ' '+ kk + ': ' + str(vv) + ' Comments Liked\n'
    return dict(m=userDict, rich = richResponse)


def specificLikesRec():
    userDict = groupMeFeatures.specificLikesRec(session.dictComments, session.translator)
    richResponse = 'Secret Crushes (Who Likes Certain Member The Most):\n\n'
    for k,v in userDict.iteritems():
        richResponse += k + "'s Secret Admirers:\n"
        limit = 0
        for kk,vv in  sorted(v.items(), key=lambda x: x[1], reverse=True):
            limit += 1
            if limit > 3:
                break
            richResponse += ' '+ kk + ': ' + str(vv) + ' Comments Liked\n'
    return dict(m=userDict, rich = richResponse)

def groupMedals():
    numUsers = len(groupMe.getListOfUsers(session.myAuth,session.myGroupID))
    userDict,medalRange = groupMeFeatures.getMedalCount("", session.dictComments, session.translator,numUsers)
    return dict(r=medalRange,m=userDict)
