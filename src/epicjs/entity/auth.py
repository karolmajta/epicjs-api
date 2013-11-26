'''
Created on 3 lis 2013

@author: karol
'''
import time
import uuid
from random import choice
from string import letters

from passlib.hash import sha1_crypt  # @UnresolvedImport


class User():
    
    def __init__(self, username, password, is_admin=False):
        self.username = username
        self.salt = "".join(choice(letters) for _ in range(22)) 
        self.password_hash = self.hash_password(password)
        self.is_admin = is_admin
        self.groups = []
        self.answers = {}

    def __eq__(self, other):
        return self.username == other.username

    def hash_password(self, password):
        return sha1_crypt.encrypt(password, salt=self.salt)
    
    def check_password(self, password):
        expected_hash = self.hash_password(password)
        return self.password_hash == expected_hash


class Token():
    
    def __init__(self, user, uid_c=uuid.uuid4, timestamp_c=time.time):
        tstamp = str(timestamp_c())
        uid_str = str(uid_c())
        self.user = user
        self.key = u"{0}-{1}".format(uid_str, tstamp)
    
    def __eq__(self, other):
        return self.key == other.key


class Group():
    
    def __init__(self, name):
        self.name = name
        self.users = []
    
    def __eq__(self, other):
        return self.name == other.name