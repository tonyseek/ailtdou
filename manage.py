#!/usr/bin/env python

from flask.ext.script import Manager

from ailtdou.app import create_app


app = create_app()
manager = Manager(app)


if __name__ == '__main__':
    manager.run()
