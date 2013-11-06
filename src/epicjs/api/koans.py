'''
Created on 6 lis 2013

@author: karol
'''
from flask.ext import restful  # @UnresolvedImport

from epicjs.dao.koans import Meditation


class MeditationList(restful.Resource):
    
    def get(self):
        try:
            meditations = list(Meditation.collection().values())
            return [m.slug for m in meditations]
        except Exception as e:
            print e