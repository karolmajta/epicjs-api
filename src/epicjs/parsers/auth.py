from flask.ext.restful import reqparse  # @UnresolvedImport


credentials_parser = reqparse.RequestParser()
credentials_parser.add_argument(
    'username',
    type=str,
    required=True,
    location='args',
)
credentials_parser.add_argument(
    'password',
    type=str,
    required=True,
    location='args'
)