'''
Created on 6 lis 2013

@author: karol
'''
from flask.ext.restful import fields  # @UnresolvedImport


token_fields = {
    'key': fields.String,
    'user': fields.Nested({
        'username': fields.String,
        'is_admin': fields.String,
        'groups': fields.List(fields.Nested({
            'name': fields.String,
        })),
    }),
}