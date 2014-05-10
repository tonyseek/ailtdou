#!/usr/bin/env python

from flask.ext.script import Manager
from flask.ext.script.commands import Clean, ShowUrls

from ailtdou.app import create_app


app = create_app()
manager = Manager(app)

manager.add_command(Clean())
manager.add_command(ShowUrls())


if __name__ == '__main__':
    manager.run()
