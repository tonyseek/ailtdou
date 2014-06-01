#!/usr/bin/env python

from flask.ext.script import Manager
from flask.ext.script.commands import Clean, ShowUrls
from flask.ext.migrate import MigrateCommand

from ailtdou.app import create_app
from ailtdou.main.models import inbox as _inbox


app = create_app()
manager = Manager(app)

manager.add_command(Clean())
manager.add_command(ShowUrls())
manager.add_command('db', MigrateCommand)


@manager.command
def inbox(address='0.0.0.0', port=4467):
    """Watches inbox and handles incoming requests."""
    _inbox.serve(int(port), address)


if __name__ == '__main__':
    manager.run()
