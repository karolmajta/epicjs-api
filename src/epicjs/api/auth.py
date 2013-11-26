from flask import g

from flask.ext.restful import marshal  # @UnresolvedImport

from epicjs.dao.auth import User, Token
from epicjs.parsers.auth import credentials_parser
from epicjs.api.decorators import authenticate
from epicjs.serializers.auth import token_fields
from epicjs.api.commons import CorsResource


class CurrentToken(CorsResource):
    
    
    def retrieve(self):
        credentials = credentials_parser.parse_args()  # @UndefinedVariable
        user = User.get(credentials['username'])
        if not user: return {"detail": "Not found"}, 404
        if not user.check_password(credentials['password']): return {"detail": "Forbidden"}, 403
        token = Token(user)
        token.save()
        return marshal(token, token_fields)


class TokenDetail(CorsResource):
    
    @authenticate
    def destroy(self, key):
        token = Token.get(key)
        if not token: return {"detail": "Not found"}, 404
        if token.user != g.user: return {"detail": "Forbidden"}, 403
        token.delete()
        return {}, 202