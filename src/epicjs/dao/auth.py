'''
Created on 3 lis 2013

@author: karol
'''
from persistent import Persistent

from flask.ext.zodb import BTree  # @UnresolvedImport

from epicjs.entity.auth import User as UserEntity
from epicjs.entity.auth import Token as TokenEntity
from epicjs.entity.auth import Group as GroupEntity


class User(UserEntity, Persistent):
    
    class Meta:
        persist_in = BTree
        unique = ('username',)


class Token(TokenEntity, Persistent):
    
    class Meta:
        persist_in = BTree
        unique = ('key',)
        

class Group(GroupEntity, Persistent):
    
    class Meta:
        persist_in = BTree
        unique = ('name',)
    
    def add_user(self, user):
        if user not in self.users: self.users.append(user)
        if self not in user.groups: user.groups.append(self)
        self._p_changed = True
        user._p_changed = True
        
    def remove_user(self, user):
        if user in self.users: self.users.remove(user)
        if self in user.groups: user.groups.remove(self)
        self._p_changed = True
        user._p_changed = True