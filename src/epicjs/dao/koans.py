'''
Created on 5 lis 2013

@author: karol
'''
from persistent import Persistent

from flask.ext.zodb import BTree  # @UnresolvedImport

from epicjs.entity.koans import Meditation as MeditationEntity


class Meditation(Persistent, MeditationEntity):
    
    class Meta:
        persist_in = BTree
        unique = ('slug',)
    
    def add_koan(self, koan):
        koan.meditation = self
        self.koans.append(koan)
        self._p_changed = True
    
    def drop_koan(self, name):
        self.koans = filter(lambda n: n != name, self.koans)
        self._p_changed = True