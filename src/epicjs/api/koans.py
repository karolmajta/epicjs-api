'''
Created on 6 lis 2013

@author: karol
'''
from flask import g, request

from flask.ext.restful import marshal # @UnresolvedImport

from epicjs.dao.koans import Meditation
from epicjs.serializers.koans import meditation_list_fields,\
    meditation_detail_fields
from epicjs.api.commons import CorsResource
from epicjs.api.decorators import authenticate
from epicjs.entity.koans import Answer
from epicjs.parsers.koans import answer_parser
from epicjs.api.utils import get_user_from_request

                
class MeditationList(CorsResource):
    
    def retrieve(self):
        
        meditations = list(Meditation.collection().values())
        s = sorted(meditations, key=lambda m: m.slug)
        return [marshal(m, meditation_list_fields) for m in s]


class MeditationDetail(CorsResource):

    def extend_with_null_solutions(self, koans):
        for koan in koans:
            koan.answer = ""
    
    def extend_with_user_solutions(self, koans, user):
        for koan in koans:
            answer = user.answers.get(koan, None)
            if answer:
                koan.answer = answer.text
            else:
                koan.answer = ""

    def retrieve(self, slug):
        meditation = Meditation.get(slug)
        if not meditation: return {"detail": "Not found"}, 404
        user = get_user_from_request(request)
        if not user:
            self.extend_with_null_solutions(meditation.koans)
        else:
            self.extend_with_user_solutions(meditation.koans, user)
        return marshal(meditation, meditation_detail_fields)


class KoanAnswer(CorsResource):
    
    @authenticate
    def create(self, meditation_slug, koan_slug):
        meditation = Meditation.get(meditation_slug)
        if not meditation: return {"detail": "Not found"}, 404
        koans = filter(lambda k: k.slug == koan_slug, meditation.koans)
        try:
            koan = koans[0]
        except IndexError:
            return {"detail": "Not found"}, 404
        answer = answer_parser.parse_args()  # @UndefinedVariable
        new_answer = Answer(koan, answer['answer'])
        g.user.add_answer(new_answer)
        return {}, 201