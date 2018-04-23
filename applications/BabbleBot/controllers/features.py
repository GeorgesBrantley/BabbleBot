# -*- coding: utf-8 -*-
import groupMeFeaturesMatt
import groupMeFeaturesRonak
import groupMeFeatures
import groupMe
import operator
import plotly.plotly as py
import plotly.graph_objs as go

def sumOfLikesinGroup():
    # Has a corresponding view
    # gets values from Sessions
    if session.myAuth is None or groupMe.checkValidAuth(session.myAuth) is False:
        redirect(URL('auth','index'))
    comments = session.dictComments
    # sends values to bigger function in groupMeFeatures.py
    sumLikes = groupMeFeatures.getSumofLikes(comments)
    # shows output on view
    return dict(sum = sumLikes)

def groupMarkov():
    # Display Markov Chains for entire Group
    if session.myAuth is None or groupMe.checkValidAuth(session.myAuth) is False:
        redirect(URL('auth','index'))
    comments = session.dictComments # get comments
    results = groupMeFeatures.createMarkChain('all',10,comments)
    richResponse = []
    for x in results:
        richResponse.append('Group Markov Chain: ' + x)
    return dict(marks = results, rich = richResponse)


def likesRecievedPerUser():
    if session.myAuth is None or groupMe.checkValidAuth(session.myAuth) is False:
        redirect(URL('auth','index'))
    userDict = groupMeFeatures.getLikesPerUser(session.dictComments, session.translator)
    richResponse = 'Member Rankings by Total Likes Recieved:\n\n'
    names = []
    values = []
    for k,v in sorted(userDict.items(), key=lambda x: x[1], reverse=True):
        richResponse += k + ': ' + str(v) + ' Total Likes Recieved\n'
        names.append(k)
        values.append(int(v))
    fig = {
    'data': [{'labels': names,
              'values': values,
              'text': names,
              'type': 'pie'}],
    'layout': {'title': 'Likes Received'}}

    graphLink = py.plot(fig)
    return dict(m=userDict, rich = richResponse, graphLink = graphLink + '.png')

def numComments():
    if session.myAuth is None or groupMe.checkValidAuth(session.myAuth) is False:
        redirect(URL('auth','index'))
    coms = session.dictComments
    #id = inout
    #inputId = 19191585
    ans = groupMeFeatures.countCommentsPerUser(coms, session.translator)
    richResponse = 'Number Of Comments Per Member:\n'
    names = []
    values = []
    for k,v in sorted(ans.items(), key=lambda x: x[1], reverse=True):
        richResponse += k + ' has ' + str(v) + ' Comments!\n'
        names.append(k)
        values.append(int(v))

    fig = {
    'data': [{'labels': names,
              'values': values,
               'text': names,
              'type': 'pie'}],
    'layout': {'title': 'Number of comments'}}

    graphLink = py.plot(fig)

    return dict(ans=ans, gn = session.groupName, rich = richResponse, graphLink = graphLink + '.png')

def pastName():
    if session.myAuth is None or groupMe.checkValidAuth(session.myAuth) is False:
        redirect(URL('auth','index'))
    coms = session.dictComments
    oldNames,newNames = groupMeFeatures.getPastName(coms)
    richRes = "Past Names of Members\n\n"
    y = 0
    for x in oldNames:
        richRes += x + " --> " + newNames[y] + "\n"
        y += 1
    return dict(past = oldNames, future = newNames, rich = richRes)

def numKicked():
    if session.myAuth is None or groupMe.checkValidAuth(session.myAuth) is False:
        redirect(URL('auth','index'))
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
    if session.myAuth is None or groupMe.checkValidAuth(session.myAuth) is False:
        redirect(URL('auth','index'))
    userDict = groupMeFeatures.mostGivingUsers(session.dictComments, session.translator)
    richResponse = 'Member Rankings by Total Likes Given:\n\n'
    names = []
    values = []
    for k,v in sorted(userDict.items(), key=lambda x: x[1], reverse=True):
        richResponse += k + ': ' + str(v) + ' Total Likes Given\n'
        names.append(k)
        values.append(int(v))
    fig = {
    'data': [{'labels': names,
              'values': values,
              'text': names,
              'type': 'pie'}],
    'layout': {'title': 'Likes Given'}}

    graphLink = py.plot(fig)
    return dict(m=userDict, rich = richResponse, graphLink = graphLink + '.png')

def likesPerComment():
    if session.myAuth is None or groupMe.checkValidAuth(session.myAuth) is False:
        redirect(URL('auth','index'))
    ratio = groupMeFeatures.getLikesPerComment(session.dictComments,session.translator)
    richResponse = 'Member Rankings by Average Likes Per Comment:\n\n'
    names = []
    values = []
    for k,v in sorted(ratio.items(), key=lambda x: x[1], reverse=True):
        richResponse += k + ': ' + str(v) + ' Likes/Comment\n'
        if float(v) > 0:
            names.append(k)
            values.append(float(v))

    x = names
    y = values

    data = [go.Bar(
            x=x,
            y=y,
            text=y,
            textposition = 'auto',
            marker=dict(
                color='rgb(158,202,225)',
                line=dict(
                    color='rgb(8,48,107)',
                    width=1.5),
            ),
            opacity=0.6
        )]
    layout = go.Layout(
        title='Rankings by Likes Per Comment',
        )
    fig = go.Figure(data=data, layout=layout)
    graphLink = py.plot(fig)
    return dict(m=ratio, rich = richResponse, graphLink = graphLink + '.png')

def specificLikes():
    if session.myAuth is None or groupMe.checkValidAuth(session.myAuth) is False:
        redirect(URL('auth','index'))
    # a user's secret crush
    userDict = groupMeFeatures.specificLikesGiven(session.dictComments, session.translator)
    richResponse = 'Secret Crushes (Who Users Like The Most):\n\n'
    for k,v in userDict.iteritems():
        richResponse += '\n' + k + "'s Secret Crushes:\n"
        limit = 0
        for kk,vv in  sorted(v[0].items(), key=lambda x: x[1], reverse=True):
            limit += 1
            if limit > 3:
                break
            richResponse += kk + ': ' + str(vv) + ' Comments Liked\n'
    return dict(m=userDict, rich = richResponse)


def specificLikesRec():
    if session.myAuth is None or groupMe.checkValidAuth(session.myAuth) is False:
        redirect(URL('auth','index'))
    userDict = groupMeFeatures.specificLikesRec(session.dictComments, session.translator)
    richResponse = 'Secret Crushes (Who Likes Certain Member The Most):\n\n'
    for k,v in userDict.iteritems():
        richResponse += '\n' + k + "'s Secret Admirers:\n"
        limit = 0
        for kk,vv in  sorted(v[0].items(), key=lambda x: x[1], reverse=True):
            limit += 1
            if limit > 3:
                break
            richResponse +=  kk + ': ' + str(vv) + ' Comments Liked\n'
    return dict(m=userDict, rich = richResponse)

def groupMedals():
    if session.myAuth is None or groupMe.checkValidAuth(session.myAuth) is False:
        redirect(URL('auth','index'))
    numUsers = len(groupMe.getListOfUsers(session.myAuth,session.myGroupID))
    userDict,medalRange = groupMeFeatures.getMedalCount("", session.dictComments, session.translator,numUsers)
    # Create Responses
    richPlatResponse = 'Platinum Medals (100% Likes):\n'
    richGoldResponse = 'Gold Medals (75% Likes):\n'
    richSilvResponse = 'Silver Medals (50% Likes):\n'
    richBronResponse = 'Bronze Medals (25% Likes):\n'

    medals = ['Platinum','Gold','Silver','Bronze']
    richResponses = [richPlatResponse,richGoldResponse,richSilvResponse,richBronResponse]
    right = 0
    for mm in medals:
        for k,vv in sorted(userDict.items(), key=lambda x: x[1][mm], reverse=True):
            if vv[mm] != 0:
                richResponses[right] += k + ' Has Earned ' + str(vv[mm]) + ' ' + mm
                if vv[mm] > 1:
                    richResponses[right] += ' Medals!\n'
                else:
                    richResponses[right] += 'Medal!\n'
        right += 1

    colors = ['#e5e4e2','#DAA520','#C0C0C0','#cd7f32']
    return dict(r=medalRange,m=userDict,medals=medals, gn = session.groupName, riches = richResponses, colors=colors)

def curseWords():
    if session.myAuth is None or groupMe.checkValidAuth(session.myAuth) is False:
        redirect(URL('auth','index'))
    curseWords = groupMeFeaturesMatt.getCommonCurseWords(session.dictComments, session.translator)
    richResponse = 'Most common curse words in group:\n\n'
    count = 0
    for word, list in sorted(curseWords.iteritems(), key=lambda x: x[1], reverse=True):
        number = list[0]
        if count <= 2:
            richResponse += word + ': ' + str(number) + ' \n'
        count += 1
    richResponse += '\n'
    count = 0
    for word, info in sorted(curseWords.iteritems(), key=lambda x: x[1], reverse=True):
        if count <= 2:
            userList = info[1]
            richResponse += 'Top Users of ' + word.upper() + ' \n'
            for user, count in sorted(userList.iteritems(), key=lambda x: x[1], reverse=True):
                richResponse += user + ': ' + str(count) + ' \n'
            richResponse += '\n'
        count += 1

    return dict(m=curseWords, rich = richResponse)

def mostLikedComments():
    if session.myAuth is None or groupMe.checkValidAuth(session.myAuth) is False:
        redirect(URL('auth','index'))
    likedCommentsDict = groupMeFeatures.getMostLikedComments(session.dictComments, session.translator)
    richResponse = 'Top 10 Most Liked Comments:\n\n'
    x = 0
    summedComments = []
    for k,v in sorted(likedCommentsDict.items(), key=lambda x:x[1][1], reverse=True):
        richResponse += v[2].encode('utf-8') + '('+str(v[1])+" Likes): " + v[0].encode('utf-8') +  '\n'
        summedComments.append([v[2],v[1],v[0]])
        x += 1
        if x > 9:
            break

    return dict(m=summedComments, rich = richResponse)

def mostUsedWord():
    if session.myAuth is None or groupMe.checkValidAuth(session.myAuth) is False:
        redirect(URL('auth','index'))
    sWord = request.vars.sWord
    # Do not display the table if no word has been inputted.
    if sWord == '' or sWord == None:
        return dict(w=0)
    #Check for malicious input
    if not groupMe.checkInput(sWord):
        redirect(URL('mostUsedWord'))

    userDict = groupMeFeaturesRonak.mostUsedWord(session.dictComments, session.translator,sWord)
    richResponse = 'Amount of Times Users have Said "' +sWord+'":\n\n'
    totalCount = 0 # The total amount of times a word has been said.
    for k,v in sorted(userDict.items(), key=lambda x: x[1], reverse=True):
        richResponse += k + ' has said it ' + str(v) + ' times!\n'
        totalCount += v
    return dict(w=1, m=userDict, rich=richResponse, word = sWord, t=totalCount)

def graph_mostGivingUsers():
    if session.myAuth is None or groupMe.checkValidAuth(session.myAuth) is False:
        redirect(URL('auth','index'))
    userDict = groupMeFeatures.mostGivingUsers(session.dictComments, session.translator)
    richResponse = 'Member Rankings by Total Likes Given:\n\n'
    for k,v in sorted(userDict.items(), key=lambda x: x[1], reverse=True):
        richResponse += k + ': ' + str(v) + ' Total Likes Given\n'
    return dict(m=userDict, rich = richResponse)

def gender():
    userNames = []
    for i,n in session.translator.iteritems():
        if len(str(i)) > 6 and i != 'system' and i != 'calendar':
            userNames.append([n,i])
    # usernames is a list of lists
    # userNames[0] = [name, id]
    return dict(userNames = userNames)

def sexismTracker():
    genderDict = dict(request.vars)
    sexisms = groupMeFeatures.getSexismTracker(session.dictComments, session.translator, genderDict)

    richResponse = 'BabbleBot Sexism Tracker (Male Comments/Female Comments: ' + str(sexisms[1]) + '):\n'
    richResponse += 'Higher Ratios -> More likely to like Male Comments\n\n'
    for k,v in sorted(sexisms[0].items(), key=lambda x: x[1][3], reverse=True):
        richResponse += k + ': ' + str(v[3]) + ' Sexism Ratio\n'
    return dict(s = sexisms[0], r = sexisms[1], gn = session.groupName, rich = richResponse)

def bestFriends():
    bestFriends = groupMeFeaturesMatt.getBestFriends(session.dictComments, session.translator)

    richResponse = 'Best Friends Ranking:\n'
    for user, list in sorted(bestFriends.items(), key=lambda x: x[1][1], reverse=True):
        richResponse += user + ': ' + list[0] + '(' + str(list[1]) + ')\n'

    return dict(f = bestFriends, rich = richResponse)

def allComments():
    if session.myAuth is None or groupMe.checkValidAuth(session.myAuth) is False:
        redirect(URL('auth','index'))
    commentsDict = groupMeFeatures.getAllComments(session.dictComments, session.translator, user = 'ALL')
    richResponse = 'All Comments:\n\n'
    return dict(m=commentsDict, rich = richResponse)
