from flask.ext.script import Command  # @UnresolvedImport
from flask.ext.script import Option  # @UnresolvedImport

from epicjs.dao.auth import User
from epicjs.reader import parse_meditation
from epicjs.dao.koans import Meditation


class AddUser(Command):
    "Adds user with given username to database."

    option_list = (
        Option('username'),
        Option('password'),
        Option('-a', '--admin', dest='is_admin', required=False, default=False, action='store_true')
    )

    def run(self, username, password, is_admin=False):
        if User.get(username):
            print "User with given username already exists"
        else:
            user = User(username, password)
            user.save()


class DropUser(Command):
    "Removes user with given username from database"
    
    option_list = (
        Option('username'),
    )
    
    def run(self, username):
        u = User.get(username)
        if u:
            u.delete()
        else:
            print "User with given username not found"


class AddMeditation(Command):
    "Adds a meditation from given file to database"
    
    option_list = (
        Option("filepath"),
    )
    
    def run(self, filepath):
        try:
            with open(filepath, 'r') as fp:
                source_lines = fp.readlines()
        except IOError:
            print "Could not read contents of file"
            return
        try:
            meditation = parse_meditation(source_lines)
        except Exception:
            print "Could not parse meditation."
            return
        if Meditation.get(meditation.name):
            print "Meditation `{0}` already exists.".format(meditation.slug)
        meditation.save()


class DropMeditation(Command):
    "Removes a meditation with name starting with given string"
    
    option_list = (
        Option("slug"),
    )
    
    def run(self, slug):
        matches = filter(lambda m: m.slug.startswith(slug), Meditation.collection().values())
        if len(matches) == 0:
            print "No meditation matches given name"
        elif len(matches) > 1:
            print "Multiple matches:"
            for m in matches: print "\t{0}".format(m.slug)
        else:
            matches[0].delete()