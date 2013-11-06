from flask import g, abort

from flask.ext import restful  # @UnresolvedImport
from flask.ext.restful import marshal_with  # @UnresolvedImport

from epicjs.dao.auth import User, Token
from epicjs.parsers.auth import credentials_parser
from epicjs.api.decorators import authenticate
from epicjs.serializers.auth import token_fields


class CurrentToken(restful.Resource):
    
    @marshal_with(token_fields)
    def get(self):
        credentials = credentials_parser.parse_args()  # @UndefinedVariable
        user = User.get(credentials['username'])
        if not user: abort(404)
        if not user.check_password(credentials['password']): abort(403)
        token = Token(user)
        token.save()
        return token


class TokenDetail(restful.Resource):
    
    @authenticate
    def delete(self, key):
        token = Token.get(key)
        if not token: abort(404)
        if token.user != g.user: abort(403)
        token.delete()