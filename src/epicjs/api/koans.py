'''
Created on 6 lis 2013

@author: karol
'''
from flask import abort

from flask.ext.restful import marshal, marshal_with  # @UnresolvedImport

from epicjs.dao.koans import Meditation
from epicjs.serializers.koans import meditation_list_fields,\
    meditation_detail_fields
from epicjs.api.commons import CorsResource

                
class MeditationList(CorsResource):
    
    def retrieve(self):
        
        meditations = list(Meditation.collection().values())
        s = sorted(meditations, key=lambda m: m.slug)
        return [marshal(m, meditation_list_fields) for m in s]


class MeditationDetail(CorsResource):

    @marshal_with(meditation_detail_fields)
    def retrieve(self, slug):
        meditation = Meditation.get(slug)
        if not meditation: abort(404)
        return meditation