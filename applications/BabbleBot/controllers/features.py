# -*- coding: utf-8 -*-
import groupMeFeatures
# try something like
def index(): return dict(message="hello from features.py")


def sumOfLikesinGroup():
    # Has a corresponding view
    # gets values from Sessions
    comments = session.dictComments
    # sends values to bigger function in groupMeFeatures.py
    sumLikes = groupMeFeatures.getSumofLikes(comments)
    # shows output on view
    return dict(sum = sumLikes)
