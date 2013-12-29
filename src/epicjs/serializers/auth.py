'''
Created on 6 lis 2013

@author: karol
'''
from flask.ext.restful import fields  # @UnresolvedImport
from epicjs.fields import Unicode


token_fields = {
    'key': Unicode,
    'user': fields.Nested({
        'username': Unicode,
    }),
}