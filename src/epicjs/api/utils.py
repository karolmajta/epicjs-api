'''
Created on 8 lis 2013

@author: karol
'''
from epicjs.dao.auth import Token

HTTP_AUTH_HEADER = 'Authorization'


def get_user_from_request(request):
    header_value = request.headers.get(HTTP_AUTH_HEADER, None)
    if header_value is None: return None
    chunks = header_value.split(" ")
    if len(chunks) != 2: return None
    key = chunks[1]
    token = Token.get(key)
    if not token: return None
    return token.user