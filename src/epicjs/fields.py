'''
Created on 30 gru 2013

@author: karol
'''
from flask.ext.restful import fields  # @UnresolvedImport

class Unicode(fields.Raw):
    def format(self, value):
        return value.decode('utf-8')