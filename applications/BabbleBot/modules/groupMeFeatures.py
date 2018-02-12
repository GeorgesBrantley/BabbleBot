#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gluon import *
import os
import json


def getSumofLikes(comments):
    sumLikes = 0
    for k,val in comments.iteritems():
        try:
            v = json.loads(val)
            # operate on v
            comments.append(v['text'].encode("urf-8")+'\n')
            # find out amount of likes on this comment
            # add to sumLikes
            sumLikes = sumLikes + len(comment.get("favorited_by"))
        except:
            pass
    return sumLikes
