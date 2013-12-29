'''
Created on 2 lis 2013

@author: karol
'''
import os
import sys

from flask.ext.script import Manager # @UnresolvedImport

try:
    from epicjs.wsgi import bootstrap
except ImportError:
    # assume we're in a source checkout... We need to add our 'src' folder
    # to pythonpath
    sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
    from epicjs.wsgi import bootstrap
# at this point we either managed to fixed the imports or bailed out
# so it's safe to import other stuff the ususal way
from epicjs.commands import AddUser, DropUser, AddMeditation, DropMeditation


application = bootstrap()

epicjs_manager = Manager()
epicjs_manager.add_command('adduser', AddUser())
epicjs_manager.add_command('dropuser', DropUser())
epicjs_manager.add_command('addmeditation', AddMeditation())
epicjs_manager.add_command('dropmeditation', DropMeditation())

manager = Manager(application)
manager.add_command('epicjs', epicjs_manager)

if __name__ == "__main__":
    manager.run()