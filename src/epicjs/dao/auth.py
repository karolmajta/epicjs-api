'''
Created on 3 lis 2013

@author: karol
'''
from persistent import Persistent

from flask.ext.zodb import BTree  # @UnresolvedImport

from epicjs.entity.auth import User as UserEntity
from epicjs.entity.auth import Token as TokenEntity


class User(UserEntity, Persistent):
    
    class Meta:
        persist_in = BTree
        unique = ('username',)
        
    def add_answer(self, answer):
        self.answers[answer.koan] = answer
        self._p_changed = True


class Token(TokenEntity, Persistent):
    
    class Meta:
        persist_in = BTree
        unique = ('key',)