'''
Created on 26 lis 2013

@author: karol
'''

from flask.ext.restful import reqparse  # @UnresolvedImport


answer_parser = reqparse.RequestParser()
answer_parser.add_argument(
    'answer',
    type=str,
    required=True,
    location='json',
)
