import os
from ConfigParser import ConfigParser

from flask import Flask

from flask.ext import restful  # @UnresolvedImport

from db import storage, bootstrap_storage

import epicjs.dao.auth

from epicjs.api.auth import CurrentToken, TokenDetail
from epicjs.api.koans import MeditationList, MeditationDetail

def bootstrap(config_file=None, project_root=None):
    #####################################################################
    # Read the config file
    #####################################################################
    
    if not config_file:
        config_file = os.path.join(os.getcwd(), 'epicjs-dev.cfg')
    if not os.path.exists(config_file):
        msg = "Config file not found at `{0}`".format(config_file)
        raise AssertionError(msg)
    config = ConfigParser()
    config.read(config_file)
    
    SERVER_SECRET = config.get('commons', 'secret')
    
    ZODB_URI = config.get('zodb', 'uri')  

    #####################################################################
    # Some configuration magic...
    #####################################################################
    
    if not project_root:
        project_root = os.path.dirname(config_file)
    static_root = os.path.join(project_root, 'static')
    template_root = os.path.join(project_root, 'templates')
    import_name = __name__.split('.')[0]
    
    #####################################################################
    # Bootstrap the app itself
    #####################################################################
    
    application = Flask(
        import_name=import_name,
        static_folder=static_root,
        static_url_path='/static/',
        template_folder=template_root,
    )
    
    #####################################################################
    # Add some custom config
    #####################################################################
    
    application.config['SERVER_SECRET'] = SERVER_SECRET
    
    #####################################################################
    # Bootstrap the persistence
    #####################################################################
    
    application.config['ZODB_STORAGE'] = ZODB_URI
    storage.init_app(application)  # @UndefinedVariable
    model_map = {
        'auth': epicjs.dao.auth,
        'koans': epicjs.dao.koans,
    }
    bootstrap_storage(application, storage, model_map)
    
    #####################################################################
    # Add routing
    #####################################################################
    
    api = restful.Api(application)
    api.add_resource(CurrentToken, '/token')
    api.add_resource(TokenDetail, '/tokens/<string:key>')
    api.add_resource(MeditationList, '/meditations/')
    api.add_resource(MeditationDetail, '/meditations/<string:slug>')
    
    #####################################################################
    # And allow others to mess with it :)
    #####################################################################
    
    return application