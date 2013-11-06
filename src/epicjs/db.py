'''
Created on 2 lis 2013

@author: karol
'''
import inspect

import transaction

from flask.ext.zodb import ZODB  # @UnresolvedImport
from flask.ext.zodb import Dict, BTree  # @UnresolvedImport

storage = ZODB()


def bootstrap_storage(application, storage, modules_map):
    for prefix, module in modules_map.items():
        cls = [t for t in inspect.getmembers(module, inspect.isclass)]
        cleaned = [c for c in cls if c[1].__module__ == module.__name__]
        for pc in cleaned:
            classname, klass = pc
            for_join = [prefix, classname] if prefix else [classname]    
            name = ".".join(for_join)
            with application.test_request_context():
                try:
                    storage[name]
                except KeyError:
                    storage[name] = klass.Meta.persist_in()
                    transaction.commit()
                augment_with_active_record(klass, name)

    
def augment_with_active_record(klass, collection_key):
    klass.collection_key = collection_key
    klass.get = classmethod(get)
    klass.exists = classmethod(exists)
    klass.collection = classmethod(collection)
    klass.uid = uid
    klass.exists = exists
    klass.save = save
    klass.delete = delete

#####################################################################
# Define some classmethods that will augment our models
#####################################################################

def get(klass, *args):
    search_uid = tuple(args)
    col = klass.collection()
    if isinstance(col, (Dict, BTree)):
        try:
            return col[search_uid]
        except KeyError:
            return None
    else:
        matched = filter(lambda o: o.uid() == search_uid, col)
        return matched[0] if len(matched) > 0 else None


def exists(klass, *args):
    col = klass.collection()
    if isinstance(col, (Dict, BTree)):
        return col.has_key(tuple(args))
    else:
        len(filter(lambda o: o.uid() == tuple(args), col))


def collection(klass):
    return storage[klass.collection_key]

#####################################################################
# Define some instancemethods that will augment our models
#####################################################################

def uid(_self):
    r = map(lambda p: getattr(_self, p), _self.__class__.Meta.unique)
    return tuple(r) 

def save(_self):
    col = _self.__class__.collection()
    if isinstance(col, (Dict, BTree)):
        my_uid = _self.uid()
        col.update({my_uid: _self})
    else:
        col.append(_self)

def delete(_self):
    my_uid = _self.uid()
    col = _self.__class__.collection()
    if isinstance(col, (Dict, BTree)):
        try:
            del col[my_uid]
        except KeyError:
            pass
    else:
        i = 0
        while i < len(col):
            if col[i].uid() == my_uid: col.pop(i) 
            i += 1