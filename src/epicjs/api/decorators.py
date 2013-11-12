'''
Created on 4 lis 2013

@author: karol
'''
from flask import g, request

from epicjs.api.utils import get_user_from_request

HTTP_METHODS = ['head', 'get', 'options', 'post', 'put', 'patch', 'delete']
RESPONSE_UNAUTHORIZED = ({}, 401, {'WWW-Authenticate': "Token realm=\"epicjs\""})


def authenticate(old_method):
    def new_method(_self, *args, **kwargs):
        g.user = get_user_from_request(request)
        if not g.user: return RESPONSE_UNAUTHORIZED
        return old_method(_self, *args, **kwargs)
    return new_method