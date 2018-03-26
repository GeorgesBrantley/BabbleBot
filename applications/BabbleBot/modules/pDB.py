#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gluon import *
import json
import subprocess
import os
import time

def getUser(email):
    # Is user in USERS? (Ret false if no)
    # Return info if yes!
    f = open('USERS','r')
    jj = json.load(f)
    f.close()
    if email in jj:
        return jj[email]
    else:
        return False


def makeUser(email,pass2,auth,salt):
    # is email taken?
    # if not, write them in!
    f = open('USERS','r')
    try:
        jj = json.load(f)
    except:
        jj = {}
    if email in jj:
        f.close()
        return False
    else:
        jj[email] = {'email':email,'pass2':pass2,'auth':auth,'salt':salt}
        f = open('USERS','w')
        json.dump(jj,f)
        f.close()
        return True
    f.close()

def getGroupBot(groupID):
    #is groupID registered (has a bot?)
    # return false if no current bot
    f = open('BOTS','r')
    jj = json.load(f)
    f.close()
    if groupID in jj:
        return jj[groupID]
    else:
        return False

def makeGroupBot(groupID,botID):
    # is group already registered?
    # if not, write them in
    f = open('BOTS','r')
    try:
        jj = json.load(f)
    except:
        jj = {}
    if groupID in jj:
        f.close()
        return False
    else:
        jj[groupID] = {'groupID':groupID,'botID':botID}
        f = open('BOTS','w')
        json.dump(jj,f)
        f.close()
        return True

def encrypt(fileName, key):
    com = 'openssl aes-256-cbc -pass pass:'+key+' -e -a -salt -in GroupMeDir/'+fileName+' -out GroupMeDir/'+fileName+'ENC '
    os.system(com)
    com = 'rm GroupMeDir/'+fileName
    os.system(com)
    #subprocess.check_call('openssl aes-256-cbc -a -salt -pass pass:'+key+' -in GroupMeDir/' +fileName + ' -out GroupMeDir/' + fileName + 'ENC',shell=True)
    #subprocess.check_output('rm GroupMeDir/'+fileName,shell=True)
    return 1

def decrypt(fileName,key):
    subprocess.check_output('openssl aes-256-cbc -pass pass:'+key+' -d -a -salt -in GroupMeDir/'+fileName+'ENC -out GroupMeDir/' + fileName,shell=True)

def refreash(fileName):
    # delete related files
    com = 'rm GroupMeDir/'+fileName
    os.system(com)
    com = 'rm GroupMeDir/'+fileName + 'ENC'
    os.system(com)
