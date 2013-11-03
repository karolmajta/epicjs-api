'''
Created on 2 lis 2013

@author: karol
'''
import inspect

from persistent import Persistent

from flask.ext.zodb import ZODB  # @UnresolvedImport
from flask.ext.zodb import BTree  # @UnresolvedImport

storage = ZODB()

def bootstrap_storage(application, storage, modules_map):
    for prefix, module in modules_map.items():
        cls = [t for t in inspect.getmembers(module, inspect.isclass)]
        persistent_cls = [c for c in cls if issubclass(c[1], Persistent)]
        cleaned = filter(lambda c: c[1] != Persistent, persistent_cls)
        with application.test_request_context():
            for pc in cleaned:
                cn = pc[0]
                for_join = [prefix, cn] if prefix else [cn]    
                name = ".".join(for_join)
                if name not in storage:
                    storage[name] = BTree
    
