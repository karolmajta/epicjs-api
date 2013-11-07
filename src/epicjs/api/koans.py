'''
Created on 6 lis 2013

@author: karol
'''
from flask import abort

from flask.ext import restful  # @UnresolvedImport
from flask.ext.restful import marshal, marshal_with  # @UnresolvedImport

from epicjs.dao.koans import Meditation
from epicjs.serializers.koans import meditation_list_fields,\
    meditation_detail_fields


class MeditationList(restful.Resource):
    
    def get(self):
        meditations = list(Meditation.collection().values())
        s = sorted(meditations, key=lambda m: m.slug)
        return [marshal(m, meditation_list_fields) for m in s]


class MeditationDetail(restful.Resource):

    @marshal_with(meditation_detail_fields)
    def get(self, slug):
        meditation = Meditation.get(slug)
        if not meditation: abort(404)
        return meditation