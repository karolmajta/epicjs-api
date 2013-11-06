'''
Created on 5 lis 2013

@author: karol
'''

class Meditation(object):
    
    def __init__(self, slug, name, koans=None):
        self.slug = slug
        self.name = name
        self.koans = koans if koans is not None else []

    def __eq__(self, other):
        return self.slug == other.slug


class Koan(object):
    
    def __init__(self, slug, name, hint, code):
        self.slug = slug
        self.name = name
        self.hint = hint
        self.code = code
        self.meditation = None
    
    def __eq__(self, other):
        return self.meditation == other.meditation and self.name == other.name


class Answer(object):
    
    def __init__(self, koan, author, text=""):
        self.koan = koan
        self.text = text
        self.author = author
    
    def __eq__(self, other):
        return self.koan == other.koan and self.author == other.author