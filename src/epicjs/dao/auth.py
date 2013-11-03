'''
Created on 3 lis 2013

@author: karol
'''
from persistent import Persistent

from ..entity.auth import User as UserEntity

class User(UserEntity, Persistent):
    pass