# -*- coding: utf-8 -*-
import groupMe
import groupMeFeatures
import pDB
import thread
import time
import json
import hashlib
import random
import string
from Crypto.Hash import SHA256
from Crypto.Cipher import AES
import binascii

# Landing page
def index():
    return dict()
def error():
    return dict()
def about():
    return dict()

def login():
    if session.email:
        redirect(URL('chooseGroup'))
    return dict(s=request.vars.success)

def checkLogin():
    # user has submitted information about their email and password
    email = request.vars.email
    passwd = request.vars.passwd
    # TODO CHECK INPUT FOR MALICIOUS CODE
    if not groupMe.checkInput(email) or not groupMe.checkInput(passwd):
        passwd = 'DDDDDDDDDDDDDDDDDDDDDDDDDDD'
        passwd = ""
        redirect(URL('login', vars=dict(success=False)))
    # check if email in database
    user = pDB.getUser(email)
    if user == False:
        redirect(URL('login', vars=dict(success=False)))
    # ADD SALT
    # hash password once and save
    saltedPassHash = hashlib.md5()
    saltedPassHash.update(passwd + user['salt'])
    saltedPassHash = saltedPassHash.hexdigest()
    
    # ZERO OUT
    passwd = 'DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD'
    passwd = ''
    # hash password again,
    doubleHashPass = hashlib.md5()
    doubleHashPass.update(saltedPassHash)
    doubleHashPass = doubleHashPass.hexdigest()
    # and compare to database, if ==, ACCOUNT LOG IN
    databasePass = user['pass2'] #GET
    if doubleHashPass != databasePass:
        # NOT EQUAL! (DELETE VARIABLES
        redirect(URL('login', vars=dict(success=False)))
    # GET ENCRYPTED AUTH FROM DATABASE
    encAuth = user['auth']
    # user passwordH1 to decrpt auth code.
    while len(saltedPassHash) < 32:
        saltedPassHash += ' '
    decryption_suite = AES.new(saltedPassHash, AES.MODE_CBC, 'This is an IV456')
    plain_auth = decryption_suite.decrypt(encAuth.decode('hex'))
    # UPDATE SESSIONS!
    session.myAuth = plain_auth[:plain_auth.find(' ')]
    # FOR GROUPME ENCR
    session.uKey = saltedPassHash
    session.accountName = email
    session.email = email.replace('@','',100)
    redirect(URL('chooseGroup'))


def register(): return dict(s=request.vars.success, m=request.vars.message)

def checkRegister():
    # user has submitted info about email, password, and auth
    email = request.vars.email
    passwd = request.vars.passwd
    inputAuth = request.vars.inAuth
    # SANTIZED TODO
    if not groupMe.checkInput(email) or not groupMe.checkInput(passwd) or not groupMe.checkInput(inputAuth):
        redirect(URL('register', vars=dict(success=False)))
    # Check if email taken in database
    # Check if password is correct size
    # check if auth is working (groupMe.py)
    if groupMe.checkValidAuth(inputAuth):
        # If YES: Register account
        # hash password twice, add to database
        saltedPassHash = hashlib.md5()
        # CREATE SALT
        salt = ''
        for x in range(0,5):
            salt += random.SystemRandom().choice(string.ascii_uppercase + string.digits)
        # Double Hash Password
        saltedPassHash.update(passwd + salt)
        passwd = 'DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD'
        passwd = ''
        saltedPassHash = saltedPassHash.hexdigest()
        # Continue Hashing
        doubleSaltedPass = hashlib.md5()
        doubleSaltedPass.update(saltedPassHash)
        doubleSaltedPass = doubleSaltedPass.hexdigest()
        # Use saltedPass1 to encrypt inputAuth
        # pad key
        while len(saltedPassHash) < 32:
            saltedPassHash += ' '
        obj = AES.new(saltedPassHash, AES.MODE_CBC, 'This is an IV456')
        while len(inputAuth) % 16 != 0:
            inputAuth += ' '
        encAuth = binascii.hexlify(obj.encrypt(inputAuth))
        # Add to DataBase!
        #return dict(e=email,p2 = doubleSaltedPass,eA = str(encAuth),s=salt)
        if not pDB.makeUser(email,doubleSaltedPass,encAuth,salt):
#             return dict(success='User Already Created')
            redirect(URL('register', vars=dict(success=False, message='User Already Created')))
        # changes flag
        flag = True
        # signs them in!
        # FIX INPUT AUTH
        session.myAuth = inputAuth[:inputAuth.find(' ')]
        inputAuth = 'DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD'
        # GET DATA FOR GROUPME
        session.uKey = saltedPassHash
        saltedPassHash = 'DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD'
        session.email = email.replace('@','',100)
        redirect(URL('chooseGroup'))
    else:
        # not good auth
        redirect(URL('register', vars=dict(success=False, message='Bad Token')))

def guest(): return dict(s=request.vars.success)

def checkGuest():
    inputAuth = request.vars.auth
    session.email = 'Guest'
    if not groupMe.checkInput(inputAuth):
        redirect(URL('guest', vars=dict(success=False)))
    # check if auth is working (groupMe.py)
    if groupMe.checkValidAuth(inputAuth):
        session.myAuth = inputAuth
        redirect(URL('chooseGroupGuest'))
    else:
        redirect(URL('guest', vars=dict(success=False)))
    return dict(success='Bad Auth')


def logOut():
    session.clear()
    redirect(URL('index'))

def chooseGroup():

    # Check if user should be on guest page
    if session.email == 'Guest':
        redirect(URL('chooseGroupGuest'))


    # GET LIST OF GROUPS!
    groups = groupMe.getAllGroups(session.myAuth)
    newComs = []
    for g in groups:
        flag = False # if encrypting is necessary
        try:
            pDB.decrypt(g['group_id']+session.email,session.uKey)
            flag = True
        except:
            pass
        newComs.append(groupMe.fileInfo(session.myAuth,g['group_id'],session.email,session.uKey))
        if flag == True:
            try:
                pDB.encrypt(g['group_id']+session.email,session.uKey)
            except:
                pass
    return dict(groups=groups, auth=session.myAuth,newComs=newComs, success=True)

def chooseGroupGuest():
    groups = groupMe.getAllGroups(session.myAuth)
    newComs = []
    for g in groups:
        numComments = groupMe.totalCommentsInGroup(session.myAuth, g['group_id'])
        newComs.append(numComments)
    return dict(groups=groups, auth=session.myAuth, newComs=newComs, success=True)
