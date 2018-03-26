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

def login():
    return dict()

def checkLogin():
    # user has submitted information about their email and password
    email = request.vars.email
    passwd = request.vars.passwd
    # TODO CHECK INPUT FOR MALICIOUS CODE
    # check if email in database
    user = pDB.getUser(email)
    if user == False:
        return dict(success='email not in database')
    # ADD SALT
    # hash password once and save
    saltedPassHash = hashlib.md5()
    saltedPassHash.update(passwd + user['salt'])
    saltedPassHash = saltedPassHash.hexdigest()
    # hash password again,
    doubleHashPass = hashlib.md5()
    doubleHashPass.update(saltedPassHash)
    doubleHashPass = doubleHashPass.hexdigest()
    # and compare to database, if ==, ACCOUNT LOG IN
    databasePass = user['pass2'] #GET
    if doubleHashPass != databasePass:
        # NOT EQUAL! (DELETE VARIABLES
        return dict(success='password Failed!')
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
    session.email = email.replace('@','',100)
    redirect(URL('chooseGroup'))


def register(): return dict()

def checkRegister():
    # user has submitted info about email, password, and auth
    email = request.vars.email
    passwd = request.vars.passwd
    inputAuth = request.vars.inAuth
    # SANTIZED TODO
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
            return dict(success='User Already Created')
        # changes flag
        flag = True
        # signs them in!
        # FIX INPUT AUTH
        session.myAuth = inputAuth[:inputAuth.find(' ')]
        # GET DATA FOR GROUPME
        session.uKey = saltedPassHash
        session.email = email.replace('@','',100)
        redirect(URL('chooseGroup'))
    else:
        # not good auth
        return dict(success='Bad Auth')

def guest(): return dict()

def chooseGroup():

    # GET LIST OF GROUPS!
    groups = groupMe.getAllGroups(session.myAuth)
    newComs = []
    for g in groups:
        try:
            pDB.decrypt(g['group_id']+session.email,session.uKey)
        except:
            pass
        newComs.append(groupMe.fileInfo(session.myAuth,g['group_id'],session.email,session.uKey))
        try:
            pDB.encrypt(g['group_id']+session.email,session.uKey)
        except:
            pass
    return dict(groups=groups, auth=session.myAuth,newComs=newComs, success=True)
