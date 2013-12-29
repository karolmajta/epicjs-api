'''
Created on 6 lis 2013

@author: karol
'''
from flask.ext.restful import fields  # @UnresolvedImport
from epicjs.fields import Unicode

meditation_list_fields = {
    'name': Unicode,
    'slug': Unicode,
}

meditation_detail_fields = {
    'name': Unicode,
    'slug': Unicode,
    'koans': fields.List(fields.Nested({
        'slug': Unicode,
        'hint': Unicode,
        'name': Unicode,
        'code': Unicode,
        'answer': Unicode,
    })),
}