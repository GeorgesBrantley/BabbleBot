# -*- coding: utf-8 -*-
import groupMeFeatures


def groupMarkov():
    # Display Markov Chains for entire Group
    comments = session.dictComments # get comments
    results = groupMeFeatures.createMarkChain('all',10,comments)
    
    return dict(marks = results)
