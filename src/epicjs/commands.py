from flask.ext.script import Command  # @UnresolvedImport


class AddUser(Command):
    "Adds user with given username to database. If no password is specified"
    "added user will have a random password"

    def run(self):
        print "hello world"