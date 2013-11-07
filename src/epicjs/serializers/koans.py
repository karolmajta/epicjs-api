'''
Created on 6 lis 2013

@author: karol
'''
from flask.ext.restful import fields  # @UnresolvedImport


meditation_list_fields = {
    'name': fields.String,
    'slug': fields.String,
}

meditation_detail_fields = {
    'name': fields.String,
    'slug': fields.String,
    'koans': fields.List(fields.Nested({
        'slug': fields.String,
        'hint': fields.String,
        'name': fields.String,
        'code': fields.String,
    })),
}