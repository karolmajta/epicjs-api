'''
Created on 4 lis 2013

@author: karol
'''
from flask import g, request
from epicjs.dao.auth import Token

HTTP_METHODS = ['head', 'get', 'options', 'post', 'put', 'patch', 'delete']
HTTP_AUTH_HEADER = 'Authorization'
RESPONSE_UNAUTHORIZED = ({}, 401, {'WWW-Authenticate': "Token realm=\"epicjs\""})


def get_user_from_request(request):
    header_value = request.headers.get(HTTP_AUTH_HEADER, None)
    if header_value is None: return None
    chunks = header_value.split(" ")
    if len(chunks) != 2: return None
    key = chunks[1]
    token = Token.get(key)
    if not token: return None
    return token.user


def authenticate(old_method):
    def new_method(_self, *args, **kwargs):
        g.user = get_user_from_request(request)
        if not g.user: return RESPONSE_UNAUTHORIZED
        return old_method(_self, *args, **kwargs)
    return new_method