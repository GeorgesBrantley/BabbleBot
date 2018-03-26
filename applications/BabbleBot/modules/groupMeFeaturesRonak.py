#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gluon import *
import json
import os
import markovify
import types

def mostUsedWord(com, translator, sWord):
    wordCount = {} # By Users!
    i = 0
    for k,val in com.iteritems():
        try:
            v = json.loads(val)
            msg = v['text'].lower().split()

            for word in msg:
                if word.lower() == sWord.lower():
                    if v['sender_id'] in wordCount and len(v['sender_id']) > 6:
                        wordCount[v['sender_id']] += 1
                    else:
                        wordCount[v['sender_id']] = 1
        except:
            pass

    translated = {}
    for k,val in wordCount.iteritems():
        translated[translator[k]] = val

    return translated
