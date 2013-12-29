'''
Created on 6 lis 2013

@author: karol
'''
from flask.ext.restful import fields  # @UnresolvedImport


token_fields = {
    'key': fields.String,
    'user': fields.Nested({
        'username': fields.String,
    }),
}